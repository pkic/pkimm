import yaml
import pandas as pd
import jsonschema
import json

# Load the YAML content from the canonical data file
model_version = '2.0.0'
file_path = f'../../data/pkimm-model-{model_version}.yaml'
with open(file_path, 'r') as file:
    data = yaml.safe_load(file)

# Sanity-check that the filename and the YAML's version field agree
if str(data.get('version')) != model_version:
    raise ValueError(
        f"Version mismatch: filename declares {model_version}, "
        f"YAML declares {data.get('version')!r}"
    )

# Load the JSON schema
schema_file_path = '../../data/pkimm-model.schema-2.0.0.json'
with open(schema_file_path, 'r') as schema_file:
    schema = json.load(schema_file)

# Validate the YAML content against the schema
try:
    jsonschema.validate(data, schema)
    print("Validation successful")
except jsonschema.ValidationError as e:
    print(f"Validation error: {e.message}")

# Load the references catalog and build a lookup dict by id
refs_catalog = yaml.safe_load(open('../../data/pkimm-references.yaml'))['references']
ref_by_id = {r['id']: r for r in refs_catalog}


def resolve_references(ref_ids):
    """Resolve a list of catalog reference IDs into a formatted string matching
    the 1.0.0 CSV style: one '- Title' line per reference (no URLs)."""
    if not ref_ids:
        return ''
    lines = []
    for ref_id in ref_ids:
        ref = ref_by_id.get(ref_id)
        if ref:
            lines.append(f"- {ref['title']}")
        else:
            lines.append(f"- {ref_id}")
    return '\n'.join(lines)


# Prepare lists to hold the structured data for the CSV
chapters = []
items = []

# Extract data according to the specified structure.
# Category IDs are kebab-case in 2.0.0; requirement IDs are also kebab-case.
# Level names are unprefixed (e.g. "Foundational"); the composed form would be
# "${number} - ${name}" but levels are not output as a column in the CSV.
for module in data.get('modules', []):
    module_id = module.get('id', '')
    for category in module.get('categories', []):
        chapter_id = f"{module_id}.{category.get('id', '')}"
        chapter_name = category.get('name', '')
        chapter_description = category.get('description', '')
        for requirement in category.get('requirements', []):
            item_id = f"{chapter_id}.{requirement.get('id', '')}"
            item_name = requirement.get('description', '')
            item_description = requirement.get('guidance', '')
            assessment = requirement.get('assessment', '')
            references = requirement.get('references', [])
            resolved_refs = resolve_references(references)
            item_additional_info = f"Assessment\n{assessment}\nReferences\n{resolved_refs}"

            # Append the data to the lists
            chapters.append([chapter_id, chapter_name, chapter_description])
            items.append([item_id, item_name, item_description, item_additional_info])

# Convert the lists to dataframes
chapters_df = pd.DataFrame(chapters, columns=["Chapter ID", "Chapter Name", "Chapter Description"])
items_df = pd.DataFrame(items, columns=["Item ID", "Item Name", "Item Description", "Item Additional Information"])

# Extract the chapter ID part from item ID (everything before the last dot-segment)
items_df['Chapter ID'] = items_df['Item ID'].apply(lambda x: '.'.join(x.split('.')[:-1]))

# Merge the dataframes on Chapter ID to get the final structure
result_df = pd.merge(chapters_df, items_df, on="Chapter ID")

# Remove duplicate rows from the dataframe
result_df.drop_duplicates(inplace=True)

# Save the final dataframe to CSV without the header
csv_file_path_no_header = f'pkimm-{model_version}.csv'
result_df.to_csv(csv_file_path_no_header, index=False, header=False, lineterminator='\n')

# Provide the path for download
print(f"Output written to: {csv_file_path_no_header}")
