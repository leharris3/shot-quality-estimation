import os
import ffmpeg
import logging

from extract_rs_shots import (
    save_shot_clip,
)
from utils.truncate import (
    read_video_to_tensor_buffer,
    pred_conf_scores,
    get_highest_conf_idx,
)

from utils.config import *

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_shot_subdir(action_name):
    logging.debug(f"Determining subdir for action: {action_name}")
    if "+" in action_name:
        return MADE_SHOT_SUBDIR
    elif "-" in action_name:
        return MISSED_SHOT_SUBDIR
    else:
        return None

def shot_exists(dst_dir, clip_name):
    logging.debug(f"Checking if shot exists in {dst_dir} for clip {clip_name}")
    for subdir_check in [MADE_SHOT_SUBDIR, MISSED_SHOT_SUBDIR, GARBAGE_SUBDIR]:
        if os.path.isfile(os.path.join(dst_dir, subdir_check, clip_name)):
            logging.info(f"Shot {clip_name} exists in {subdir_check}")
            return True
    return False

def get_video_aspect_ratio(video_fp):
    logging.debug(f"Getting aspect ratio for video: {video_fp}")
    probe = ffmpeg.probe(video_fp)
    video_stream = next((stream for stream in probe["streams"] if stream["codec_type"] == "video"), None)
    if not video_stream:
        logging.error("No video stream found in the input file.")
        raise ValueError("No video stream found in the input file.")
    aspect_ratio = int(video_stream["width"]) / int(video_stream["height"])
    logging.info(f"Aspect ratio for video {video_fp}: {aspect_ratio}")
    return aspect_ratio

def save_and_process_shot(video_fp, dst_path, start_time, aspect_ratio, row, dst_dir, device, model):
    logging.debug(f"Saving and processing shot from {video_fp} to {dst_path}")
    save_shot_clip(video_fp, dst_path, start_time, TEMP_SHOT_DURATION_SEC, height=TARGET_HEIGHT, aspect_ratio=aspect_ratio)

    video_tensor = read_video_to_tensor_buffer(dst_path)
    if video_tensor is None:
        logging.warning(f"Failed to read video tensor from {dst_path}")
        return

    # remove the original clip
    os.remove(dst_path)
    logging.debug(f"Removed original clip {dst_path}")

    conf_scores, timestamps = pred_conf_scores(video_tensor, device=device, model=model, step_size=STEP)

    try:
        max_idx = get_highest_conf_idx(conf_scores, sigma=SIGMA)
    except Exception as e:
        logging.warning(f"Failed to get highest conf idx: {e}")
        return
    
    logging.info(f"Max confidence index: {max_idx}")

    if max_idx > 0 and max_idx < len(timestamps):
        split_point_sec = timestamps[max_idx] + OUT_SHOT_OFFSET_SEC
    else:
        logging.warning(f"Max-conf idx: {max_idx}, out of range. Skipping shot at: {dst_path}")
        return

    new_start_time = start_time + split_point_sec - OUT_SHOT_DURATION_SEC
    adj_idx = (STEP * max_idx) + OUT_SHOT_OFFSET_NUM_FRAMES
    subdir = determine_subdir(adj_idx, row.action_name)

    new_dst_path = os.path.join(dst_dir, subdir, os.path.basename(dst_path))
    logging.debug(f"New destination path: {new_dst_path}")

    save_shot_clip(video_fp, new_dst_path, new_start_time, OUT_SHOT_DURATION_SEC, height=TARGET_HEIGHT, aspect_ratio=aspect_ratio)
    logging.debug(f"Saved processed shot to {new_dst_path}")

def determine_subdir(adj_idx, action_name):
    logging.debug(f"Determining subdir with adj_idx: {adj_idx}, action_name: {action_name}")
    if adj_idx <= LOW_NOISE_IDX or adj_idx >= TEMP_VID_NUM_FRAMES - HIGH_NOISE_IDX:
        return GARBAGE_SUBDIR
    if "+" in action_name:
        return MADE_SHOT_SUBDIR
    elif "-" in action_name:
        return MISSED_SHOT_SUBDIR
    return None
