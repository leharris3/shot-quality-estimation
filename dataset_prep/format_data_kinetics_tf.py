import os
import csv
import pandas as pd
import subprocess
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


def is_mp4_and_valid(file_path):
    """Check if the file is an MP4 and can be opened with ffmpeg."""
    if not file_path.endswith(".mp4"):
        return False
    try:
        result = subprocess.run(
            ["ffmpeg", "-i", file_path], stderr=subprocess.PIPE, stdout=subprocess.PIPE
        )
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def clean_file(file_path):
    """Check and remove the file if it is not a valid MP4."""
    if not is_mp4_and_valid(file_path):
        print(f"Removing invalid or non-MP4 file: {file_path}")
        os.remove(file_path)


def clean_directory(dir_path):
    """Iterate over all files in the directory and its subdirectories, and delete non-valid MP4 files using multithreading."""
    files_to_check = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            files_to_check.append(file_path)

    with ThreadPoolExecutor(max_workers=1) as executor:
        list(tqdm(executor.map(clean_file, files_to_check), total=len(files_to_check)))


def format_dataset_kinetics(dir_path):
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
                labels.append(1 if label == "shot_result" else 0)
        df = pd.DataFrame(
            {
                "c1": fps,
                "c2": labels,
            }
        )
        df.to_csv(csv_path, index=False, index_label=False, header=False, sep=" ")


if __name__ == "__main__":
    dir_path = "/playpen-storage/levlevi/contextualized-shot-quality-analysis/basketball-shot-detection/data/experiments/result-only/shot_results_nba_1k"
    clean_directory(dir_path)
    # format_dataset_kinetics(dir_path)
