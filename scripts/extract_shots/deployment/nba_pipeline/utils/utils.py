import os
import ffmpeg

from extract_rs_shots import (
    save_shot_clip,
)
from utils.truncate import (
    read_video_to_tensor_buffer,
    pred_conf_scores,
    get_highest_conf_idx,
)

from utils.config import *

def get_shot_subdir(action_name):
    if "+" in action_name:
        return MADE_SHOT_SUBDIR
    elif "-" in action_name:
        return MISSED_SHOT_SUBDIR
    else:
        return None

def shot_exists(dst_dir, clip_name):
    for subdir_check in [MADE_SHOT_SUBDIR, MISSED_SHOT_SUBDIR, GARBAGE_SUBDIR]:
        if os.path.isfile(os.path.join(dst_dir, subdir_check, clip_name)):
            return True
    return False

def get_video_aspect_ratio(video_fp):
    probe = ffmpeg.probe(video_fp)
    video_stream = next((stream for stream in probe["streams"] if stream["codec_type"] == "video"), None)
    if not video_stream:
        raise ValueError("No video stream found in the input file.")
    return int(video_stream["width"]) / int(video_stream["height"])

def save_and_process_shot(video_fp, dst_path, start_time, aspect_ratio, row, dst_dir, device, model):
    save_shot_clip(video_fp, dst_path, start_time, TEMP_SHOT_DURATION_SEC, height=TARGET_HEIGHT, aspect_ratio=aspect_ratio)

    video_tensor = read_video_to_tensor_buffer(dst_path, device=device)
    if video_tensor is None:
        return

    os.remove(dst_path)

    try:
        conf_scores, timestamps = pred_conf_scores(video_tensor, device=device, model=model, step_size=STEP)
        max_idx = get_highest_conf_idx(conf_scores, sigma=2)
        split_point_sec = timestamps[max_idx] + OUT_SHOT_OFFSET_SEC
    except (ValueError, IndexError) as e:
        print(f"{e} \n Skipping shot with id: {os.path.basename(dst_path)}")
        return

    new_start_time = start_time + split_point_sec - OUT_SHOT_DURATION_SEC

    adj_idx = (STEP * max_idx) + OUT_SHOT_OFFSET_NUM_FRAMES
    subdir = determine_subdir(adj_idx, row.action_name)

    new_dst_path = os.path.join(dst_dir, subdir, os.path.basename(dst_path))

    try:
        save_shot_clip(video_fp, new_dst_path, new_start_time, OUT_SHOT_DURATION_SEC, height=TARGET_HEIGHT, aspect_ratio=aspect_ratio)
    except Exception as e:
        print(f"{e} \n Error processing video at {new_dst_path}")

def determine_subdir(adj_idx, action_name):
    if adj_idx <= LOW_NOISE_IDX or adj_idx >= TEMP_VID_NUM_FRAMES - HIGH_NOISE_IDX:
        return GARBAGE_SUBDIR
    if "+" in action_name:
        return MADE_SHOT_SUBDIR
    elif "-" in action_name:
        return MISSED_SHOT_SUBDIR
    return None