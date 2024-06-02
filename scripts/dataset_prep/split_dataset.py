import os
import shutil
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

FILE_SIZE_THRESH = 1  # Threshold in KB (adjusted to match 100 KB)
MAX_THREADS = 8  # Increase the number of threads to improve concurrency
NUM_CLIPS = 50000

def remove_small_files(files):
    """
    Given a list of files, remove all files under a threshold of 100 KB
    """
    trunc_fps = [file for file in files if os.stat(file).st_size / 1000 >= FILE_SIZE_THRESH]
    for file in files:
        if file not in trunc_fps:
            os.remove(file)
    return trunc_fps

def copy_file(src, dst, progress_bar=None):
    """
    Copy a single file from src to dst
    """
    shutil.copy2(src, dst)
    if progress_bar:
        progress_bar.update(1)

def copy_and_split_dataset(
    train_val_src_dir: str,
    test_dir: str,
    dst_dir: str,
    num_files_to_copy: int,
    class_split=None,
    class_balance=None,
):
    # default 90/10 train/val
    if class_split is None:
        class_split = [0.9, 0.1]
    if class_balance is None:
        class_balance = [0.5, 0.5]

    # Collect all source file paths
    all_src_file_paths = [
        os.path.join(root, file)
        for root, _, files in os.walk(train_val_src_dir)
        for file in files if file.endswith(".mp4")
    ]

    made_file_paths = []
    missed_file_paths = []

    for index, src_file_path in enumerate(all_src_file_paths):
        file_name = os.path.basename(src_file_path)
        file_class = os.path.basename(os.path.dirname(src_file_path))

        # Split exactly into 90/10 train/val
        split_dir = "val" if index % int(class_split[0] * 10) == 0 else "train"
        dst_file_path = os.path.join(dst_dir, split_dir, file_class, file_name)

        if file_class == "made":
            made_file_paths.append((src_file_path, dst_file_path))
        elif file_class == "missed":
            missed_file_paths.append((src_file_path, dst_file_path))

    random.shuffle(made_file_paths)
    random.shuffle(missed_file_paths)

    # Copy clips proportional to class balance: [made, missed]
    all_copy_operations = (
        made_file_paths[: int(class_balance[0] * num_files_to_copy)] +
        missed_file_paths[: int(class_balance[1] * num_files_to_copy)]
    )

    # Add all file paths from the test folder
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.endswith(".mp4"):
                src_test_file_path = os.path.join(root, file)
                file_name = os.path.basename(src_test_file_path)
                file_class = os.path.basename(os.path.dirname(src_test_file_path))
                dst_test_file_path = os.path.join(dst_dir, "test", file_class, file_name)
                all_copy_operations.append((src_test_file_path, dst_test_file_path))

    # Make new train/val/test dirs
    split_dirs = ["train", "val", "test"]
    for split_dir in split_dirs:
        os.makedirs(os.path.join(dst_dir, split_dir, "made"), exist_ok=True)
        os.makedirs(os.path.join(dst_dir, split_dir, "missed"), exist_ok=True)

    # Copy files using ThreadPoolExecutor with progress bar
    with tqdm(total=len(all_copy_operations)) as progress_bar:
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            future_to_copy = {executor.submit(copy_file, src, dst, progress_bar): (src, dst) for src, dst in all_copy_operations}
            for future in as_completed(future_to_copy):
                future.result()  # Ensure exceptions are raised if any