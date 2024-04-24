import os
import shutil
import random

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
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
        file_size = os.stat(file).st_size / 1000 # kbs
        if file_size < FILE_SIZE_THRESH:
            os.remove(file)
        else:
            trunc_fps.append(file)
    return trunc_fps

def copy_file(args, progress=None):
    """
    Copy a single file from (src, dst)
    """

    src, dst = args
    shutil.copy2(src, dst)
    # except Exception as e:
    #     print(f"Error copying file from {src}.")
    
    # iterate the progress bar
    if progress:
        progress.update(1)

def split_dataset(src_dir, dst_dir, num_clips):
    """
    Given a path to a dir w/ 'made' and 'missed' subdirs,
    split data into train/val/test subdirs with a ratio of
    80/15/5 into the dst_dir
    """

    og_vid_fps = []
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.mp4'):
                fp = os.path.join(root, file)
                og_vid_fps.append(fp)

    # remove all files under 100kb in size
    og_vid_fps = remove_small_files(og_vid_fps)
    split_dirs = ['train', 'val', 'test']

    # make new train/val/test dirs
    os.makedirs(dst_dir, exist_ok=True)
    for sd in split_dirs:
        new_dir = os.path.join(dst_dir, sd)
        os.makedirs(new_dir, exist_ok=True)

        os.makedirs(os.path.join(new_dir, 'made'), exist_ok=True)
        os.makedirs(os.path.join(new_dir, 'missed'), exist_ok=True)

        # os.makedirs(os.path.join(new_dir, 'noise'), exist_ok=True)
        # os.makedirs(os.path.join(new_dir, 'shot_result'), exist_ok=True)

    # shuffle file paths
    random.shuffle(og_vid_fps)
    og_vid_fps = og_vid_fps[0:num_clips]

    copy_ops = []
    for fp in og_vid_fps:
        seed = random.random()
        name = fp.split('/')[-1]
        split_dir = ''
        cat = fp.split('/')[-2]
        if seed < .8:
            split_dir = 'train'
        elif seed < .95:
            split_dir = 'val'
        else:
            split_dir = 'test'

        # new_fp = os.path.join(dst_dir, split_dir, cat, name)

        # copy to made/missed folder, no split
        new_fp = os.path.join(dst_dir, cat, name)
        copy_ops.append((fp, new_fp))

    progress = tqdm(total=len(copy_ops))

    # copy each file in a different process pool
    with ThreadPoolExecutor(max_workers=1) as executor:
        for op in copy_ops:
            executor.submit(copy_file, op, progress=progress)