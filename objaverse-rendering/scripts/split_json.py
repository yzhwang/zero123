import json

def split_json_file(input_file: str, output_prefix: str, num_splits: int):
    with open(input_file, 'r') as f:
        data = json.load(f)

    chunk_size = len(data) // num_splits
    data_items = list(data.items())

    for i in range(num_splits):
        start = i * chunk_size
        end = start + chunk_size if i < num_splits - 1 else len(data)
        chunk = dict(data_items[start:end])

        output_file = f"{output_prefix}_{i+1}.json"
        with open(output_file, 'w') as f:
            json.dump(chunk, f, indent=4)

        print(f"Created file {output_file} with {len(chunk)} items")


# Example usage
input_file = "object-paths.json"
output_prefix = "split_file"
num_splits = 8

split_json_file(input_file, output_prefix, num_splits)

