import glob
import json
import multiprocessing
import shutil
import subprocess
import time
from dataclasses import dataclass
from typing import Optional
import os

import boto3
import tyro
import math


@dataclass
class Args:
    workers_per_gpu: int
    """number of workers per gpu"""

    input_models_path: str
    """Path to a json file containing a list of 3D object files"""

    upload_to_s3: bool = False
    """Whether to upload the rendered images to S3"""

    num_gpus: int = -1
    """number of gpus to use. -1 means all available gpus"""


def worker(
    queue: multiprocessing.JoinableQueue,
    count: multiprocessing.Value,
    gpu: int,
    s3: Optional[boto3.client],
) -> None:
    while True:
        item = queue.get()
        if item is None:
            break

        # Perform some operation on the item
        print(item, gpu)
        command = (
            f"export DISPLAY=:0.{gpu} &&"
            f" sudo blender-3.2.2-linux-x64/blender -b -P scripts/blender_script.py --"
            f" --object_path {item}"
        )
        print(command)

        # Run the subprocess and wait for completion
        process = subprocess.run(command, shell=True, stderr=subprocess.PIPE, text=True)

        # Check if Blender process finished successfully
        if process.returncode != 0:
            print(f"Error: {process.stderr}")

        with count.get_lock():
            count.value += 1

        queue.task_done()


if __name__ == "__main__":
    args = tyro.cli(Args)

    queue = multiprocessing.JoinableQueue()
    count = multiprocessing.Value("i", 0)

    # Start worker processes on each of the GPUs
    for gpu_i in range(args.num_gpus):
        for worker_i in range(args.workers_per_gpu):
            worker_i = gpu_i * args.workers_per_gpu + worker_i
            process = multiprocessing.Process(
                target=worker, args=(queue, count, gpu_i, None)
            )
            process.daemon = True
            process.start()

    # Add items to the queue
    with open(args.input_models_path, "r") as f:
        model_paths = json.load(f)

    input_dir = os.path.dirname(args.input_models_path)
    cnt = 0
    for item in model_paths:
        if cnt == 10000:
            break
        print(model_paths[item])
        queue.put(os.path.join(input_dir,model_paths[item]))
        cnt+=1

    # Wait for all tasks to be completed
    queue.join()

    # Add sentinels to the queue to stop the worker processes
    for i in range(args.num_gpus * args.workers_per_gpu):
        queue.put(None)
