import os
import pandas as pd
import subprocess
import shlex

from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


def is_mp4_and_valid(file_path):
    if os.path.getsize(file_path) <= 1000:
        return False  # File is too small, likely corrupted or blank
    
    command = f"ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {shlex.quote(file_path)}"
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    _, stderr = process.communicate()
    stderr = stderr.decode("utf-8")
    if "moov atom not found" in stderr:
        return False
    if os.path.getsize(file_path) <= 1000:
        return False  # File is too small, likely corrupted or blank
    return True


def clean_file(file_path):
    """Check and remove the file if it is not a valid MP4."""
    if not is_mp4_and_valid(file_path):
        print(f"Removing invalid or non-MP4 file: {file_path}")
        os.remove(file_path)


def clean_directory(dir_path):
    """Iterate over all files in the directory and its subdirectories, and delete non-valid MP4 files using multithreading."""
    files_to_check = (os.path.join(root, file)
                      for root, _, files in os.walk(dir_path)
                      for file in files if file.endswith(".mp4"))

    with ThreadPoolExecutor(max_workers=8) as executor:
        list(tqdm(executor.map(clean_file, files_to_check)))


def format_dataset_kinetics(dir_path: str):
    """
    Given a path to a dataset split into train/val/test subdirs,
    produce three files: train.csv, val.csv, test.csv.

    All files saved to `dir_path`.
    Based on [this](https://github.com/facebookresearch/TimeSformer/blob/main/timesformer/datasets/DATASET.md) guide.
    """

    train_dir = os.path.join(dir_path, "train")
    val_dir = os.path.join(dir_path, "val")
    test_dir = os.path.join(dir_path, "test")
    subdirs = [train_dir, val_dir, test_dir]

    for sd, split in zip(subdirs, ["train", "val", "test"]):
        csv_path = os.path.join(dir_path, f"{split}.csv")
        fps = []
        labels = []
        for root, _, files in os.walk(sd):
            for file in files:
                fp = os.path.join(root, file)
                abs_path = os.path.abspath(fp)
                label = fp.split("/")[-2]
                fps.append(abs_path)
                labels.append(1 if label == "made" else 0)
        df = pd.DataFrame(
            {
                "c1": fps,
                "c2": labels,
            }
        )
        df.to_csv(csv_path, index=False, index_label=False, header=False, sep=" ")