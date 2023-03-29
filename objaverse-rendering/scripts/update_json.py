import os
import glob
import json

root_directory = 'rendered_views'

# Get subfolder names and store them in a set
subfolder_names = set()
for entry in os.scandir(root_directory):
    if entry.is_dir():
        subfolder_names.add(entry.name)

# Iterate through each JSON file
for i in range(1, 9):
    json_filename = f'split_file_{i}.json'
    new_json_filename = f'split_file_new_{i}.json'

    # Read the JSON file
    with open(json_filename, 'r') as json_file:
        data = json.load(json_file)

    # Remove keys present in the subfolder_names set
    for key in subfolder_names:
        if key in data:
            del data[key]

    # Write the updated dictionary back to the JSON file
    with open(new_json_filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

