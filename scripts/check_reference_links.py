#!/usr/bin/env python3
"""Check that every URL in the references catalog still resolves.

Manual-run, not a CI gate. Some publishers (ISO, PCI SSC) refuse automated
clients while serving the same documents fine in a browser, so those responses
are reported as their own class instead of counting as failures.

Exits non-zero only when a URL is genuinely broken."""
from __future__ import annotations
import argparse
import dataclasses
import enum
import functools
import http.client
import ssl
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable, Iterable

import yaml

try:
    import certifi
except ImportError:  # pragma: no cover - certifi is a declared dependency
    certifi = None


DEFAULT_CATALOG = "data/pkimm-references.yaml"
DEFAULT_TIMEOUT = 30.0
DEFAULT_WORKERS = 8
# One retry is enough to ride out a momentary blip without slowing a clean run.
DEFAULT_ATTEMPTS = 2
DEFAULT_BACKOFF = 2.0

# Without a browser user agent several publishers reject the request outright.
# NSA's CDN also refuses browser versions older than about a year, so keep the
# version current: a refused request reports a missing document as BLOCKED.
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
)
# The same CDN refuses a request that sends no Accept header.
BROWSER_ACCEPT = "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8"

# Codes that mean "a human with a browser can read this, a script cannot".
BOT_BLOCKED_CODES = frozenset({401, 403, 405, 406, 429})


class LinkStatus(enum.Enum):
    """Outcome of checking a single URL."""

    OK = "OK"
    REDIRECT = "REDIRECT"
    BLOCKED = "BLOCKED"
    BROKEN = "BROKEN"


@dataclasses.dataclass(frozen=True)
class LinkResult:
    """One catalog URL and what checking it produced."""

    ref_id: str
    url: str
    status: LinkStatus
    detail: str = ""


class FetchError(Exception):
    """The URL could not be reached at all: DNS failure, timeout, refused connection."""


# A fetcher takes a URL and returns (HTTP status code, final URL after redirects).
Fetcher = Callable[[str], tuple[int, str]]


def certifi_bundle() -> str | None:
    """Path to the certifi CA bundle, or None when certifi is not installed."""
    return certifi.where() if certifi else None


@functools.lru_cache(maxsize=1)
def trust_context() -> ssl.SSLContext:
    """Build the TLS context used for every request.

    Some Python builds — notably the python.org macOS ones — ship without a
    usable OpenSSL trust store, which makes every HTTPS URL in the catalog look
    broken. Preferring the certifi bundle avoids that false result. Falls back to
    the interpreter default, which is correct where the system store works."""
    return ssl.create_default_context(cafile=certifi_bundle())


def http_fetcher(url: str, timeout: float = DEFAULT_TIMEOUT) -> tuple[int, str]:
    """Fetch `url` and report its status code and the URL it ended up at.

    The response body is never read — only the headers are needed, and several
    catalog entries point at large PDFs."""
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": BROWSER_USER_AGENT, "Accept": BROWSER_ACCEPT},
            method="GET",
        )
        with urllib.request.urlopen(request, timeout=timeout, context=trust_context()) as response:
            return response.status, response.geturl()
    except urllib.error.HTTPError as exc:
        # An error response is still an answer about the URL, so report the code.
        return exc.code, exc.url or url
    except (
        urllib.error.URLError, OSError, ValueError, http.client.HTTPException
    ) as exc:
        # ValueError covers a url urllib rejects before any I/O; HTTPException covers
        # http.client.InvalidURL, which subclasses neither OSError nor ValueError and
        # would otherwise abort the whole scan over one bad entry.
        raise FetchError(f"{type(exc).__name__}: {exc}") from exc


def check_url(
    ref_id: str,
    url: str,
    fetcher: Fetcher,
    attempts: int = DEFAULT_ATTEMPTS,
    backoff: float = DEFAULT_BACKOFF,
) -> LinkResult:
    """Classify one catalog URL.

    A timeout, DNS hiccup or 5xx says nothing about whether the document is
    still published, so those are retried before being called broken. A 4xx is
    a definite answer and is never retried."""
    if not url:
        return LinkResult(ref_id, url, LinkStatus.OK, "no url")

    for remaining in range(max(attempts, 1) - 1, -1, -1):
        try:
            status_code, final_url = fetcher(url)
        except FetchError as exc:
            if remaining:
                time.sleep(backoff)
                continue
            return LinkResult(ref_id, url, LinkStatus.BROKEN, f"unreachable: {exc}")
        if status_code >= 500 and remaining:
            time.sleep(backoff)
            continue
        break

    # Where a redirect landed is the best lead for fixing an entry whose
    # publisher moved the document.
    landed = f" after redirect to {final_url}" if final_url and final_url != url else ""
    if status_code in BOT_BLOCKED_CODES:
        return LinkResult(
            ref_id, url, LinkStatus.BLOCKED,
            f"HTTP {status_code}{landed}, verify in a browser",
        )
    if not 200 <= status_code < 300:
        return LinkResult(ref_id, url, LinkStatus.BROKEN, f"HTTP {status_code}{landed}")
    if final_url != url:
        return LinkResult(ref_id, url, LinkStatus.REDIRECT, f"redirects to {final_url}")
    return LinkResult(ref_id, url, LinkStatus.OK)


def load_catalog_urls(catalog_path: Path) -> list[tuple[str, str]]:
    """Return (id, url) for every entry in the catalog, in file order."""
    catalog = yaml.safe_load(catalog_path.read_text()) or {}
    return [
        (ref["id"], ref.get("url", ""))
        for ref in catalog.get("references", []) or []
        if isinstance(ref, dict) and "id" in ref
    ]


def check_catalog(
    catalog_path: Path,
    fetcher: Fetcher = http_fetcher,
    workers: int = DEFAULT_WORKERS,
    attempts: int = DEFAULT_ATTEMPTS,
    backoff: float = DEFAULT_BACKOFF,
) -> list[LinkResult]:
    """Check every URL in the catalog, preserving file order in the results."""
    entries = load_catalog_urls(catalog_path)
    if not entries:
        return []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(lambda e: check_url(e[0], e[1], fetcher, attempts, backoff), entries))


def format_report(results: Iterable[LinkResult]) -> str:
    """Render results grouped by status, most actionable first."""
    results = list(results)
    lines: list[str] = []
    for status in (LinkStatus.BROKEN, LinkStatus.REDIRECT, LinkStatus.BLOCKED, LinkStatus.OK):
        matching = [r for r in results if r.status is status]
        if not matching:
            continue
        lines.append(f"\n{status.value} ({len(matching)})")
        for result in matching:
            suffix = f" — {result.detail}" if result.detail else ""
            lines.append(f"  {result.ref_id}: {result.url}{suffix}")
    broken = sum(1 for r in results if r.status is LinkStatus.BROKEN)
    lines.append(f"\n{len(results)} url(s) checked, {broken} broken")
    return "\n".join(lines).lstrip("\n")


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", default=DEFAULT_CATALOG)
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    args = parser.parse_args()

    catalog_path = Path(args.catalog)
    if not catalog_path.exists():
        print(f"Catalog not found: {catalog_path}")
        return 1

    results = check_catalog(catalog_path, workers=args.workers)
    print(format_report(results))
    return 1 if any(r.status is LinkStatus.BROKEN for r in results) else 0


if __name__ == "__main__":
    sys.exit(_main())
