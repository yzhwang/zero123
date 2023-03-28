import json
import subprocess
import os
import concurrent.futures

import tyro
from dataclasses import dataclass
from typing import Optional

import boto3

@dataclass
class Args:
    input_models_path: str
    """Path to a json file containing a list of 3D object files"""

    gpu: int = 0
    """GPU to use for rendering"""

    concurrent_blenders: int = 4
    """Number of Blender instances to run simultaneously"""


def render_file(item: str, gpu: int) -> None:
    print(item, gpu)
    command = (
        f"export DISPLAY=:0.{gpu} &&"
        f" sudo blender-3.2.2-linux-x64/blender -b -P scripts/blender_script.py --"
        f" --gpu_index {gpu} --object_path {item}"
    )
    print(command)

    process = subprocess.run(command, shell=True, stderr=subprocess.PIPE, text=True)

    if process.returncode != 0:
        print(f"Error: {process.stderr}")


if __name__ == "__main__":
    args = tyro.cli(Args)

    with open(args.input_models_path, "r") as f:
        model_paths = json.load(f)

    input_dir = os.path.dirname(args.input_models_path)

    # Use ProcessPoolExecutor with k concurrent workers
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.concurrent_blenders) as executor:
        # Iterate through model_paths and submit render tasks
        futures = [executor.submit(render_file, os.path.join(input_dir, model_paths[item]), args.gpu) for item in model_paths]

        # Wait for all tasks to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")

