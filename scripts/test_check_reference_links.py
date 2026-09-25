"""Tests for the references catalog link checker.

The fetcher is injected in every test, so no test reaches the network."""
from __future__ import annotations
import textwrap
from pathlib import Path

import pytest

from scripts import check_reference_links as links
from scripts.check_reference_links import (
    FetchError,
    LinkStatus,
    check_catalog,
    check_url,
    format_report,
    load_catalog_urls,
)


SAMPLE_CATALOG = textwrap.dedent("""\
    schemaVersion: "1.0.0"
    version: "1.0.0"
    references:
      - id: "good-entry"
        title: "Reachable"
        url: "https://example.org/good"
      - id: "moved-entry"
        title: "Moved"
        url: "https://example.org/moved"
      - id: "blocked-entry"
        title: "Bot blocked"
        url: "https://example.org/blocked"
      - id: "gone-entry"
        title: "Gone"
        url: "https://example.org/gone"
""")


def _fetcher(responses: dict[str, tuple[int, str]]):
    """Build a fetcher backed by a fixed URL -> (status, final url) mapping."""

    def fetch(url: str) -> tuple[int, str]:
        if url not in responses:
            raise FetchError("no route to host")
        return responses[url]

    return fetch


def _all_four_statuses():
    """Fetcher covering the sample catalog with one url of each status class."""
    return _fetcher({
        "https://example.org/good": (200, "https://example.org/good"),
        "https://example.org/moved": (200, "https://example.org/final"),
        "https://example.org/blocked": (403, "https://example.org/blocked"),
        "https://example.org/gone": (404, "https://example.org/gone"),
    })


def _write_catalog(tmp_path: Path, body: str = SAMPLE_CATALOG) -> Path:
    catalog = tmp_path / "pkimm-references.yaml"
    catalog.write_text(body)
    return catalog


def test_reachable_url_is_ok() -> None:
    fetch = _fetcher({"https://example.org/good": (200, "https://example.org/good")})
    result = check_url("good-entry", "https://example.org/good", fetch)
    assert result.status is LinkStatus.OK
    assert result.detail == ""


def test_redirect_reports_the_final_url() -> None:
    fetch = _fetcher({"https://example.org/moved": (200, "https://example.org/final")})
    result = check_url("moved-entry", "https://example.org/moved", fetch)
    assert result.status is LinkStatus.REDIRECT
    assert "https://example.org/final" in result.detail


@pytest.mark.parametrize("code, status", [(404, LinkStatus.BROKEN), (403, LinkStatus.BLOCKED)])
def test_redirect_ending_in_an_error_names_where_it_went(code: int, status: LinkStatus) -> None:
    """A publisher that moved a document redirects the old url; where it landed
    is the best lead for fixing the entry."""
    fetch = _fetcher({"https://example.org/moved": (code, "https://example.org/new-home")})
    result = check_url("moved-entry", "https://example.org/moved", fetch, backoff=0)
    assert result.status is status
    assert "https://example.org/new-home" in result.detail


@pytest.mark.parametrize("code", [401, 403, 405, 406, 429])
def test_bot_protection_is_blocked_not_broken(code: int) -> None:
    """ISO and PCI SSC answer automated clients this way while serving the same
    document fine in a browser."""
    fetch = _fetcher({"https://example.org/blocked": (code, "https://example.org/blocked")})
    result = check_url("blocked-entry", "https://example.org/blocked", fetch)
    assert result.status is LinkStatus.BLOCKED
    assert str(code) in result.detail


@pytest.mark.parametrize("code", [404, 410, 500, 503])
def test_error_response_is_broken(code: int) -> None:
    fetch = _fetcher({"https://example.org/gone": (code, "https://example.org/gone")})
    result = check_url("gone-entry", "https://example.org/gone", fetch, backoff=0)
    assert result.status is LinkStatus.BROKEN
    assert str(code) in result.detail


def test_unreachable_host_is_broken() -> None:
    result = check_url("gone-entry", "https://example.org/gone", _fetcher({}), backoff=0)
    assert result.status is LinkStatus.BROKEN
    assert "unreachable" in result.detail


def test_entry_without_url_is_not_a_failure() -> None:
    result = check_url("no-url-entry", "", _fetcher({}))
    assert result.status is LinkStatus.OK


def test_load_catalog_urls_preserves_file_order(tmp_path: Path) -> None:
    catalog = _write_catalog(tmp_path)
    assert [ref_id for ref_id, _ in load_catalog_urls(catalog)] == [
        "good-entry",
        "moved-entry",
        "blocked-entry",
        "gone-entry",
    ]


def test_load_catalog_urls_skips_malformed_entries(tmp_path: Path) -> None:
    catalog = _write_catalog(
        tmp_path,
        textwrap.dedent("""\
            schemaVersion: "1.0.0"
            version: "1.0.0"
            references:
              - id: "kept"
                url: "https://example.org/kept"
              - "a bare string, not a mapping"
              - title: "no id at all"
        """),
    )
    assert load_catalog_urls(catalog) == [("kept", "https://example.org/kept")]


def test_empty_catalog_yields_no_results(tmp_path: Path) -> None:
    catalog = _write_catalog(tmp_path, 'schemaVersion: "1.0.0"\nversion: "1.0.0"\nreferences: []\n')
    assert check_catalog(catalog, fetcher=_fetcher({})) == []


def test_check_catalog_classifies_every_entry(tmp_path: Path) -> None:
    catalog = _write_catalog(tmp_path)
    fetch = _all_four_statuses()
    results = check_catalog(catalog, fetcher=fetch, workers=2, backoff=0)
    assert [r.status for r in results] == [
        LinkStatus.OK,
        LinkStatus.REDIRECT,
        LinkStatus.BLOCKED,
        LinkStatus.BROKEN,
    ]


def test_report_leads_with_broken_and_counts_them(tmp_path: Path) -> None:
    catalog = _write_catalog(tmp_path)
    fetch = _all_four_statuses()
    report = format_report(check_catalog(catalog, fetcher=fetch, workers=2, backoff=0))
    assert report.startswith("BROKEN (1)")
    assert "gone-entry" in report
    assert "4 url(s) checked, 1 broken" in report


def test_report_omits_empty_status_groups(tmp_path: Path) -> None:
    catalog = _write_catalog(tmp_path, textwrap.dedent("""\
        schemaVersion: "1.0.0"
        version: "1.0.0"
        references:
          - id: "only-good"
            url: "https://example.org/good"
    """))
    fetch = _fetcher({"https://example.org/good": (200, "https://example.org/good")})
    report = format_report(check_catalog(catalog, fetcher=fetch))
    assert "BROKEN" not in report
    assert "REDIRECT" not in report
    assert "1 url(s) checked, 0 broken" in report


class _FakeResponse:
    """Stands in for the object urlopen returns as a context manager."""

    def __init__(self, status: int, final_url: str) -> None:
        self.status = status
        self._final_url = final_url

    def geturl(self) -> str:
        return self._final_url

    def __enter__(self) -> _FakeResponse:
        return self

    def __exit__(self, *_exc_info: object) -> bool:
        return False


def test_http_fetcher_reports_status_and_final_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        links.urllib.request,
        "urlopen",
        lambda *_a, **_kw: _FakeResponse(200, "https://example.org/final"),
    )
    assert links.http_fetcher("https://example.org/start") == (200, "https://example.org/final")


def test_http_fetcher_turns_an_error_response_into_its_code(monkeypatch: pytest.MonkeyPatch) -> None:
    """A 404 is an answer about the URL, not a transport failure."""

    def raise_http_error(*_a: object, **_kw: object) -> None:
        raise links.urllib.error.HTTPError(
            "https://example.org/gone", 404, "Not Found", {}, None
        )

    monkeypatch.setattr(links.urllib.request, "urlopen", raise_http_error)
    assert links.http_fetcher("https://example.org/gone") == (404, "https://example.org/gone")


def test_http_fetcher_raises_fetch_error_when_unreachable(monkeypatch: pytest.MonkeyPatch) -> None:
    def raise_url_error(*_a: object, **_kw: object) -> None:
        raise links.urllib.error.URLError("name resolution failed")

    monkeypatch.setattr(links.urllib.request, "urlopen", raise_url_error)
    with pytest.raises(FetchError):
        links.http_fetcher("https://example.org/nowhere")


def _capture_urlopen(monkeypatch: pytest.MonkeyPatch) -> list[tuple[object, dict]]:
    """Replace urlopen with a stub that records each request and its keyword
    arguments, and answers 200 at the requested url."""
    calls: list[tuple[object, dict]] = []

    def capture(request, *_a: object, **kwargs: object) -> _FakeResponse:
        calls.append((request, kwargs))
        return _FakeResponse(200, request.full_url)

    monkeypatch.setattr(links.urllib.request, "urlopen", capture)
    return calls


def test_http_fetcher_sends_browser_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    """NSA's CDN answers 403 to a request without a current browser user agent
    and an Accept header, which reported a document that no longer exists as
    BLOCKED instead of BROKEN."""
    calls = _capture_urlopen(monkeypatch)
    links.http_fetcher("https://example.org/advisory.pdf")
    request, _kwargs = calls[0]
    assert "Mozilla/5.0" in request.get_header("User-agent")
    assert request.get_header("Accept")


def test_http_fetcher_verifies_certificates_with_the_trust_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = _capture_urlopen(monkeypatch)
    links.http_fetcher("https://example.org/advisory.pdf")
    _request, kwargs = calls[0]
    assert kwargs["context"] is links.trust_context()


def test_main_exits_non_zero_when_the_catalog_is_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(
        "sys.argv", ["check_reference_links.py", "--catalog", str(tmp_path / "absent.yaml")]
    )
    assert links._main() == 1


def test_main_exits_non_zero_on_a_broken_link(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    catalog = _write_catalog(tmp_path)
    monkeypatch.setattr("sys.argv", ["check_reference_links.py", "--catalog", str(catalog)])
    monkeypatch.setattr(
        links, "check_catalog", lambda path, **_kw: check_catalog(path, fetcher=_fetcher({}), backoff=0)
    )
    assert links._main() == 1


def test_main_exits_zero_when_every_link_resolves(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    catalog = _write_catalog(tmp_path, textwrap.dedent("""\
        schemaVersion: "1.0.0"
        version: "1.0.0"
        references:
          - id: "only-good"
            url: "https://example.org/good"
    """))
    fetch = _fetcher({"https://example.org/good": (200, "https://example.org/good")})
    monkeypatch.setattr("sys.argv", ["check_reference_links.py", "--catalog", str(catalog)])
    monkeypatch.setattr(links, "check_catalog", lambda path, **_kw: check_catalog(path, fetcher=fetch))
    assert links._main() == 0


def test_certifi_bundle_points_at_an_existing_file() -> None:
    bundle = links.certifi_bundle()
    assert bundle is not None and Path(bundle).is_file()


def test_trust_context_verifies_certificates() -> None:
    context = links.trust_context()
    assert context.verify_mode is links.ssl.CERT_REQUIRED
    assert context.check_hostname is True


def test_malformed_url_is_broken_not_a_crash() -> None:
    """urllib rejects an unparseable url with ValueError before any I/O, which
    must be reported like any other unreachable url."""
    result = check_url("bad-url-entry", "not-a-url", links.http_fetcher, backoff=0)
    assert result.status is LinkStatus.BROKEN
    assert "unreachable" in result.detail


def _counting_fetcher(outcomes: list):
    """Fetcher that walks a fixed list of outcomes, one per call."""
    calls: list[str] = []

    def fetch(url: str) -> tuple[int, str]:
        calls.append(url)
        outcome = outcomes[min(len(calls) - 1, len(outcomes) - 1)]
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    return fetch, calls


def test_transient_transport_failure_is_retried_then_succeeds() -> None:
    fetch, calls = _counting_fetcher(
        [FetchError("connection reset"), (200, "https://example.org/good")]
    )
    result = check_url("flaky", "https://example.org/good", fetch, backoff=0)
    assert result.status is LinkStatus.OK
    assert len(calls) == 2


def test_transient_server_error_is_retried_then_succeeds() -> None:
    fetch, calls = _counting_fetcher([(503, ""), (200, "https://example.org/good")])
    result = check_url("flaky", "https://example.org/good", fetch, backoff=0)
    assert result.status is LinkStatus.OK
    assert len(calls) == 2


def test_persistent_server_error_is_broken_after_all_attempts() -> None:
    fetch, calls = _counting_fetcher([(500, "https://example.org/gone")])
    result = check_url("dead", "https://example.org/gone", fetch, attempts=3, backoff=0)
    assert result.status is LinkStatus.BROKEN
    assert len(calls) == 3


def test_client_error_is_never_retried() -> None:
    """A 404 is a definite answer, so retrying it only wastes time."""
    fetch, calls = _counting_fetcher([(404, "https://example.org/gone")])
    result = check_url("dead", "https://example.org/gone", fetch, attempts=3, backoff=0)
    assert result.status is LinkStatus.BROKEN
    assert len(calls) == 1


def test_zero_attempts_still_performs_one_fetch() -> None:
    fetch, calls = _counting_fetcher([(200, "https://example.org/good")])
    result = check_url("edge", "https://example.org/good", fetch, attempts=0, backoff=0)
    assert result.status is LinkStatus.OK
    assert len(calls) == 1


@pytest.mark.parametrize(
    "url, expected_error",
    [
        ("http://[", "ValueError"),
        # A nonnumeric port raises http.client.InvalidURL, which subclasses neither
        # OSError nor ValueError, so it needs its own handler.
        ("https://example.org:notaport", "InvalidURL"),
    ],
)
def test_unparseable_url_does_not_abort_the_scan(url: str, expected_error: str) -> None:
    result = check_url("edge-entry", url, links.http_fetcher, backoff=0)
    assert result.status is LinkStatus.BROKEN
    assert expected_error in result.detail
