import json
import os
from zipfile import ZipFile
from tempfile import mkdtemp
import shutil

def update_values(obj, key, new_value):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                obj[k] = new_value
            elif isinstance(v, (dict, list)):
                update_values(v, key, new_value)
    elif isinstance(obj, list):
        for item in obj:
            update_values(item, key, new_value)

def process_file(file_path, schema_value, api_version_value):
    with open(file_path, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        update_values(data, '$schema', schema_value)
        update_values(data, 'apiVersion', api_version_value)
        f.seek(0)
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.truncate()

def update_jsons_in_zip(zip_path, output_zip_path, schema_value, api_version_value):
    temp_dir = mkdtemp(dir=os.path.dirname(output_zip_path))
    with ZipFile(zip_path) as z:
        z.extractall(temp_dir)
    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file.endswith('.json'):
                process_file(os.path.join(root, file), schema_value, api_version_value)
    with ZipFile(output_zip_path, 'w') as z:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                z.write(file_path, arcname=os.path.relpath(file_path, temp_dir))
    shutil.rmtree(temp_dir)

# Specify your paths and values here
zip_file_path = "/home/ravigzpncx/repos/staff-infrastructure-alz-terraform-policy/scripts/Diagnostic-Policy.zip"  # Update this path
output_zip_path = "/home/ravigzpncx/repos/staff-infrastructure-alz-terraform-policy/scripts/Updated-Diagnostic-Policy.zip"  # Update this path
schema_value = "http://schema.management.azure.com/schemas/2019-08-01/deploymentTemplate.json#"
api_version_value = "2021-05-01-preview"

update_jsons_in_zip(zip_file_path, output_zip_path, schema_value, api_version_value)

print(f"Updated zip file has been saved to {output_zip_path}")



