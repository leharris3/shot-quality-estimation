from tqdm import tqdm
import os
import concurrent
import pandas as pd

from concurrent.futures import ThreadPoolExecutor

from extract_rs_shots import (
    generate_file_paths,
    map_logs_to_videos,
    load_shot_attempts,
)
from truncate_clips_helpers import (
    get_model,
)
from timeout import function_with_timeout
from utils import get_video_aspect_ratio, get_shot_subdir, shot_exists, save_and_process_shot
from config import *

def run_parallel_job(dst_dir: str, hudl_logs_dir: str, videos_dir: str, num_devices: int = 1):
    if not os.path.isdir(dst_dir):
        raise ValueError(f"Destination directory {dst_dir} does not exist.")
    if not os.path.isdir(hudl_logs_dir):
        raise ValueError(f"Hudl logs directory {hudl_logs_dir} does not exist.")
    if not os.path.isdir(videos_dir):
        raise ValueError(f"Videos directory {videos_dir} does not exist.")
    if num_devices <= 0:
        raise ValueError("Number of devices must be greater than zero.")
    
    log_fps = generate_file_paths(hudl_logs_dir)
    videos_fps = generate_file_paths(videos_dir)
    logs_vids_mapped = map_logs_to_videos(videos_fps, log_fps)
    total_videos = len(logs_vids_mapped)

    if total_videos == 0:
        raise ValueError("No videos to process.")
    
    num_vids_per_device = (total_videos + num_devices - 1) // num_devices
    models = [get_model(device=device, model_path=MODEL_FP) for device in range(num_devices)]

    with ThreadPoolExecutor(max_workers=num_devices) as executor:
        processes = []
        pbar = tqdm(total=total_videos, desc="Processing Videos")  # Initialize progress bar
        for device in range(num_devices):
            start_idx = device * num_vids_per_device
            end_idx = min(start_idx + num_vids_per_device, total_videos)
            subset = logs_vids_mapped[start_idx:end_idx]
            if subset:  # Only submit if there are items to process
                model = models[device % len(models)]
                process = executor.submit(process_thread, dst_dir, subset, device, model, pbar)
                processes.append(process)
        for process in concurrent.futures.as_completed(processes):
            process.result()
        pbar.close()  # Close the progress bar when done


def process_thread(dst_dir: str, logs_vids_mapped, device: int = 0, model=None, pbar=None):
    if not model:
        raise ValueError("Model cannot be None.")
    
    for video_fp, log_fp in logs_vids_mapped:
        process_video_log_pair_result_hidden(dst_dir, video_fp, log_fp, device, model)
        if pbar:
            pbar.update(1)  # Update the progress bar


def process_video_log_pair_result_hidden(
    dst_dir: str, video_fp: str, log_fp: str, device: int = 0, model=None
):
    """
    Extract all result-hidden shot-attempts in `video_path` to `dst_dir`.
    """

    try:
        function_with_timeout(load_shot_attempts, args=(log_fp,), timeout_duration=1)
    except Exception as e:
        print(f"Error: {e}")
        return

    shot_attempts = load_shot_attempts(log_fp)
    extract_shots_result_hidden(
        dst_dir,
        shot_attempts,
        video_fp,
        device=device,
        timesformer_model=model,
    )


def extract_shots_result_hidden(dst_dir: str, shot_attempts: pd.DataFrame, video_fp: str, device: int = 0, model=None):
    """
    Extract all shots from `shot_attempts`, find the moment of shot-release, and save truncated
    shot attempts to `dst_dir`.

    Args:
        dst_dir (str): Directory where results will be saved.
        shot_attempts (DataFrame): DataFrame containing shot attempts data.
        video_fp (str): File path to the video file.
        device (int, optional): GPU ID for processing. Defaults to 0.
        model (optional): The model to use for processing video frames. Defaults to None.
    """
    period = int(video_fp.split("_period")[1].split(".mp4")[0])
    game_id = os.path.basename(video_fp).split("_")[0]
    shot_attempts_for_period = shot_attempts[shot_attempts["half"] == period]

    for _, row in tqdm(shot_attempts_for_period.iterrows(), total=shot_attempts_for_period.shape[0], desc="Processing Shots"):
        subdir = get_shot_subdir(row.action_name)
        if subdir is None:
            continue

        clip_name = f"{game_id}_{row.action_id}_{row.action_name}_{row.second}.mp4"
        dst_path = os.path.join(dst_dir, subdir, clip_name)

        if shot_exists(dst_dir, clip_name):
            continue

        start_time = row.second - TEMP_SHOT_OFFSET_SEC

        try:
            aspect_ratio = get_video_aspect_ratio(video_fp)
        except ValueError as e:
            print(f"{e} \n Error processing video at {video_fp}")
            continue

        save_and_process_shot(video_fp, dst_path, start_time, aspect_ratio, row, dst_dir, device, model)