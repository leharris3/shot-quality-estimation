import os
import pandas as pd
import ffmpeg
import concurrent.futures

from utils.paths import HUDL_LOGS_DIR, REPLAYS_DIR
from utils.timeout import function_with_timeout

OUTDIR = "/playpen-storage/levlevi/contextualized-shot-quality-analysis/data/experiments/results-shown/result_shown_nba_?k"
MADE_SUBDIR = "made"
MISSED_SUBDIR = "missed"
SHOT_DURATION_TOTAL = 7  # total clip length is 7 seconds
SHOT_DURATION_OFFSET_NEG = 5  # start clip 5 seconds before timestamps
TARGET_HEIGHT = 480
MAX_THREAD_POOL_WORKERS = 32


def generate_file_paths(directory):
    """
    Returns all file paths in the next level of `directory`.
    """

    return [os.path.join(directory, f) for f in os.listdir(directory)]


def map_logs_to_videos(video_files, log_files):
    """
    Generates a 2xN array containing `[video_fp, log_fp]` pairs.
    """

    logs_videos_paths = []
    for video_file in video_files:
        video_id = os.path.basename(video_file).split("_")[0]
        log_file = next((log for log in log_files if video_id in log), None)
        if log_file:
            logs_videos_paths.append([video_file, log_file])
    return logs_videos_paths


def load_shot_attempts(log_file_path):
    """
    Given a path to a log `log_file_path`, return a pandas df
    containing 4 columns: `['action_id', 'action_name', 'half', 'second']`.
    """

    df = pd.read_csv(log_file_path, delimiter=";")
    shots = df[df["action_name"].str.contains(r"3\+|2\+|3\-|2\-")]
    return shots[["action_id", "action_name", "half", "second"]]


def save_shot_clip(
    video_path: str,
    dst_path: str,
    start_time,
    duration,
    height=TARGET_HEIGHT,
    aspect_ratio=1,
):
    """
    Given a full video at `video_path` and a `dst_path`, sample a clip at
    `start_time` with `duration` with `target_height` and `aspect_ratio`.
    """
    
    assert os.path.isfile(video_path), f"The file {video_path} does not exist."
    new_width = int(height * aspect_ratio)
    
    # Ensure width is even multiple
    if new_width % 2 != 0:
        new_width += 1
    
    # Ensure destination directory exists
    dst_dir = os.path.dirname(dst_path)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir, exist_ok=True)
    
    try:
        ffmpeg.input(video_path, ss=start_time, t=duration).filter(
            "scale", new_width, height
        ).output(dst_path).global_args("-loglevel", "error").run()
    except Exception as e:
        print(f"Error processing video {video_path}: {e}")
        raise Exception(e)


def process_shot_attempts(shot_attempts, video_path, dst_dir):
    """
    For all shots in the df `shot_attemps`, save a video clip to `dst_dir`.
    """

    period = int(video_path.split("_period")[1].split(".mp4")[0])
    game_id = os.path.basename(video_path).split("_")[0]
    shot_attempts_for_period = shot_attempts[shot_attempts["half"] == period]

    for _, row in shot_attempts_for_period.iterrows():
        subdir = (
            MADE_SUBDIR
            if "+" in row.action_name
            else MISSED_SUBDIR if "-" in row.action_name else None
        )
        if subdir is None:
            continue

        clip_name = f"{game_id}_{row.action_id}_{row.action_name}_{row.second}.mp4"
        dst_path = os.path.join(dst_dir, subdir, clip_name)
        if os.path.exists(dst_path):
            # print(f"Clip at {dst_path} already exists.")
            continue

        start_time = row.second - SHOT_DURATION_OFFSET_NEG
        duration = SHOT_DURATION_TOTAL
        probe = ffmpeg.probe(video_path)
        video_stream = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
            None,
        )

        if not video_stream:
            raise ValueError("No video stream found in the input file.")
        aspect_ratio = int(video_stream["width"]) / int(video_stream["height"])

        save_shot_clip(
            video_path,
            dst_path,
            start_time,
            duration,
            height=TARGET_HEIGHT,
            aspect_ratio=aspect_ratio,
        )


def process_video_log_pair(video_path: str, log_path: str):
    try:
        function_with_timeout(load_shot_attempts, args=(log_path,), timeout_duration=1)
    except:
        print(f"Error reading file at {log_path}")
        return

    shot_attempts = load_shot_attempts(log_path)
    process_shot_attempts(shot_attempts, video_path, OUTDIR)


def extract_shots(hudl_logs_fps: str, videos_fps: str):
    hudl_logs_fps = generate_file_paths(HUDL_LOGS_DIR)
    videos_fps = generate_file_paths(REPLAYS_DIR)
    logs_vids_paths = map_logs_to_videos(videos_fps, hudl_logs_fps)

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_THREAD_POOL_WORKERS
    ) as executor:
        futures = []
        for video_path, log_path in logs_vids_paths:
            future = executor.submit(
                process_video_log_pair,
                video_path,
                log_path,
            )
            futures.append(future)
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                # print(f"Error processing a log")
                pass