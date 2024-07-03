import yaml
import pandas as pd
import re
import jsonschema
import json

# Load the YAML content from the uploaded file
file_path = '../../data/pkimm-model.yaml'
with open(file_path, 'r') as file:
    data = yaml.safe_load(file)

# Load the JSON schema from the uploaded file
schema_file_path = '../../data/pkimm-model.schema.json'
with open(schema_file_path, 'r') as schema_file:
    schema = json.load(schema_file)

# Validate the YAML content against the schema
try:
    jsonschema.validate(data, schema)
    print("Validation successful")
except jsonschema.ValidationError as e:
    print(f"Validation error: {e.message}")

# Function to clean the references by removing markdown links but keeping the text with dashes
def clean_references_preserve_text(ref):
    # Replace markdown links with just the text inside the brackets
    cleaned_references = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', ref)
    return cleaned_references

# Prepare lists to hold the structured data for the CSV
chapters = []
items = []

# Extract data according to the specified structure with the new Chapter ID and Item ID format
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
            references = requirement.get('references', '')
            clean_ref = clean_references_preserve_text(references)
            item_additional_info = f"Assessment\n{assessment}\nReferences\n{clean_ref}"

            # Append the data to the lists
            chapters.append([chapter_id, chapter_name, chapter_description])
            items.append([item_id, item_name, item_description, item_additional_info])

# Convert the lists to dataframes
chapters_df = pd.DataFrame(chapters, columns=["Chapter ID", "Chapter Name", "Chapter Description"])
items_df = pd.DataFrame(items, columns=["Item ID", "Item Name", "Item Description", "Item Additional Information"])

# Since the chapter IDs and item IDs are structured, we can extract the chapter ID part from item ID
items_df['Chapter ID'] = items_df['Item ID'].apply(lambda x: '.'.join(x.split('.')[:-1]))

# Merge the dataframes on Chapter ID to get the final structure
result_df = pd.merge(chapters_df, items_df, on="Chapter ID")

# Remove duplicate rows from the dataframe
result_df.drop_duplicates(inplace=True)

# Save the final dataframe to CSV without the header
csv_file_path_no_header = 'pkimm-v1.0.csv'
result_df.to_csv(csv_file_path_no_header, index=False, header=False, lineterminator='\n')

# Provide the path for download
csv_file_path_no_header
