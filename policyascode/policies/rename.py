import os

# Set the directory containing the JSON files
directory = '/home/ravigzpncx/repos/staff-infrastructure-alz-terraform-diagnostic/policyascode/policies/Diagnostics'

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith("-combined-policy.json"):
        # Extract the resource name part from the filename (e.g., "acr" from "acr-combined-policy.json")
        resource_name = filename.split("-combined-policy.json")[0]
        
        # Construct the new filename
        new_filename = f"Diagnostic-Policy-for-{resource_name}.json"
        
        # Construct the full source and destination paths
        src = os.path.join(directory, filename)
        dst = os.path.join(directory, new_filename)
        
        # Rename the file
        os.rename(src, dst)
        print(f"Renamed {filename} to {new_filename}")

print("All files have been renamed.")
