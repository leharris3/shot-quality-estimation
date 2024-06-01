import os
import shutil
import random

from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

FILE_SIZE_THRESH = 1
MAX_THREADS = 1
NUM_CLIPS = 50000


def remove_small_files(files):
    """
    Given a list of files,
    remove all files under a threshold of 100kb
    """

    trunc_fps = []
    for file in files:
        file_size = os.stat(file).st_size / 1000  # kbs
        if file_size < FILE_SIZE_THRESH:
            os.remove(file)
        else:
            trunc_fps.append(file)
    return trunc_fps


def copy_file(args, progress_bar=None):
    """
    Copy a single file from (src, dst)
    """

    src, dst = args
    shutil.copy2(src, dst)
    if progress_bar:
        progress_bar.update(1)


def copy_and_split_dataset(
    train_val_dir: str,
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

    all_src_file_paths = []
    for root, _, files in os.walk(train_val_dir):
        for file in files:
            if file.endswith(".mp4"):
                file_path = os.path.join(root, file)
                all_src_file_paths.append(file_path)

    made_file_paths = []
    missed_file_paths = []

    for (
        index,
        src_file_path,
    ) in enumerate(all_src_file_paths):
        file_name = os.path.basename(src_file_path)
        file_class = os.path.basename(os.path.dirname(src_file_path))

        # a clever way of splitting exactly into 90/10 train/val
        split_dir = "val" if index % int(class_split[0] * 10) == 0 else "train"
        dst_file_path = os.path.join(dst_dir, split_dir, file_class, file_name)

        if file_class == "made":
            made_file_paths.append([src_file_path, dst_file_path])
        elif file_class == "missed":
            missed_file_paths.append([src_file_path, dst_file_path])

    random.shuffle(made_file_paths)
    random.shuffle(missed_file_paths)

    # copy clips proptional to class balance: [made, missed]
    all_copy_opperations = (
        made_file_paths[0 : int(class_balance[0] * num_files_to_copy)]
        + missed_file_paths[0 : int(class_balance[1] * num_files_to_copy)]
    )

    # add all file paths from the test folder
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.endswith(".mp4"):
                src_test_file_path = os.path.join(root, file)
                file_name = os.path.basename(src_test_file_path)
                file_class = os.path.basename(os.path.dirname(src_test_file_path))
                split_dir = "test"
                dst_test_file_path = os.path.join(
                    dst_dir, split_dir, file_class, file_name
                )
                all_copy_opperations.append([src_test_file_path, dst_test_file_path])

    split_dirs = ["train", "val", "test"]

    # make new train/val/test dirs
    os.makedirs(dst_dir, exist_ok=True)
    for split_dir in split_dirs:
        new_dir = os.path.join(dst_dir, split_dir)
        os.makedirs(new_dir, exist_ok=True)
        os.makedirs(os.path.join(new_dir, "made"), exist_ok=True)
        os.makedirs(os.path.join(new_dir, "missed"), exist_ok=True)

    progress_bar = tqdm(total=len(all_copy_opperations))
    with ThreadPoolExecutor(max_workers=1) as executor:
        for copy_operation in all_copy_opperations:
            executor.submit(copy_file, copy_operation, progress_bar=progress_bar)
