import os
import shutil

def move_combined_policies():
    base_dir = '/home/ravigzpncx/repos/staff-infrastructure-alz-terraform-diagnostic/archivesoltecpolicy/terraform/policies'
    combined_dir = os.path.join(base_dir, 'combined')

    # Ensure the combined directory exists
    if not os.path.exists(combined_dir):
        os.makedirs(combined_dir)
        print(f"Created directory: {combined_dir}")

    # Walk through the base directory
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith("-combined-policy.json"):
                source_path = os.path.join(root, file)
                destination_path = os.path.join(combined_dir, file)

                # Move the file
                shutil.move(source_path, destination_path)
                print(f"Moved: {source_path} to {destination_path}")

if __name__ == "__main__":
    move_combined_policies()
