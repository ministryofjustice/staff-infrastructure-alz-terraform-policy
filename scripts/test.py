import os
import json

# Define the base directory where the policies folder is located
base_dir = '/home/ravigzpncx/repos/staff-infrastructure-alz-terraform-diagnostic/archivesoltecpolicy/terraform/policies'

# Loop through each subdirectory in the base directory
for resource_type in os.listdir(base_dir):
    resource_dir = os.path.join(base_dir, resource_type)
    if os.path.isdir(resource_dir):
        # Initialize a template for the combined policy
        combined_policy = {
            "name": f"{resource_type}-policy",
            "type": "Microsoft.Authorization/policyDefinitions",
            "properties": {
                "displayName": f"{resource_type.capitalize()} Policy",
                "description": f"Policy for {resource_type}.",
                "mode": "All",  # Adjust as necessary
                "metadata": {
                    "version": "1.0.0",
                    "category": resource_type.capitalize()
                },
                # These will be filled in from the files
                "parameters": {},
                "policyRule": {}
            }
        }

        # Attempt to read the parameters.json and rule.json files
        try:
            with open(os.path.join(resource_dir, 'parameters.json'), 'r') as param_file:
                combined_policy['properties']['parameters'] = json.load(param_file)

            with open(os.path.join(resource_dir, 'rule.json'), 'r') as rule_file:
                combined_policy['properties']['policyRule'] = json.load(rule_file)

            # Write the combined policy to a new JSON file
            combined_file_path = os.path.join(resource_dir, f"{resource_type}-combined-policy.json")
            with open(combined_file_path, 'w') as combined_file:
                json.dump(combined_policy, combined_file, indent=4)

            print(f"Combined policy file created at: {combined_file_path}")

        except IOError as e:
            print(f"Error reading parameters.json or rule.json in {resource_dir}: {e}")
