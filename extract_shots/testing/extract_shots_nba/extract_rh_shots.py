import os
import concurrent
import ffmpeg
import pandas as pd
import json

from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from extract_rs_shots import (
    generate_file_paths,
    map_logs_to_videos,
    load_shot_attempts,
    save_shot_clip,
    MADE_SUBDIR,
    MISSED_SUBDIR,
)
from truncate_clips_helpers import (
    get_model,
    read_video_to_tensor_buffer,
    pred_conf_scores,
    get_highest_conf_idx,
)
from paths import LOCAL_DIR
from timeout import function_with_timeout

MODEL_FP = "/playpen-storage/levlevi/contextualized-shot-quality-analysis/data/experiments/_timesformer_/__runs__/result-noise-cls/nba_result_cls_baseline_3k_32_frames_224/checkpoints/checkpoint_epoch_00020.pyth"

# fps for original and truncated video
FPS = 30

# temp clip start time: timestamp (given by logs) - 5.0s
TEMP_SHOT_OFFSET_SEC = 5

# duration of temp clip
TEMP_SHOT_DURATION_SEC = 7

# duration of final truncated clip
OUT_SHOT_DURATION_SEC = 4

# truncate original video 1.0s before max_conf timestamp
OUT_SHOT_OFFSET_SEC = 1

MADE_SHOT_SUBDIR = "made"
MISSED_SHOT_SUBDIR = "missed"
GARBAGE_SUBDIR = "garbage"

# length of inputs processed by TimeSformer model
MODEL_NUM_FRAMES = 32

# total frame count of temp vid
TEMP_VID_NUM_FRAMES = int(TEMP_SHOT_DURATION_SEC * FPS)

# final output video height, og aspect ratio maintained
TARGET_HEIGHT = 480

STEP = 5
SIGMA = 9
THREADS = 1


def generate_predictions_from_src_paths_and_basenames(
    src_paths_and_basenames: list,
    device: int = 0,
):
    timesformer_model = get_model(model_path=MODEL_FP, device=device)
    preds = {}
    conf_scores_dict = {}
    for src_path, _ in tqdm(src_paths_and_basenames, desc="Predicting", unit="video"):
        video_tensor = read_video_to_tensor_buffer(src_path, device=device)
        (
            conf_scores,
            _,
        ) = pred_conf_scores(
            video_tensor, device=device, model=timesformer_model, step_size=STEP
        )
        max_idx = get_highest_conf_idx(conf_scores, sigma=SIGMA)
        preds[src_path] = max_idx

        # convert tensors to dict
        conf_scores_dict[src_path] = [
            conf_score.tolist()[0] for conf_score in conf_scores
        ]
    return preds, conf_scores_dict


def predict_timestamps_dir(dir_path: str, max_processes: int = 1):

    def get_all_src_paths_and_basenames(src_dir: str):
        fps_names = []
        for root, _, files in os.walk(src_dir):
            for file in files:
                if file.endswith(".mp4"):
                    src_fp = os.path.join(root, file)
                    fps_names.append((src_fp, file))
        return fps_names

    src_paths_and_names = get_all_src_paths_and_basenames(dir_path)
    num_paths = len(src_paths_and_names)
    num_paths_per_worker = num_paths // max_processes

    preds = {}
    conf_scores = {}

    # break up clips into batches, use seperate processes
    with ProcessPoolExecutor(max_workers=max_processes) as executor:
        procceses = []
        for device in range(max_processes):
            start_idx = device * num_paths_per_worker
            end_idx = min(start_idx + num_paths_per_worker, len(src_paths_and_names))
            src_paths_and_names_subset = src_paths_and_names[start_idx:end_idx]
            process = executor.submit(
                generate_predictions_from_src_paths_and_basenames,
                src_paths_and_names_subset,
                device=device,
            )
            procceses.append(process)
        for process in concurrent.futures.as_completed(procceses):
            preds.update(process.result()[0])
            conf_scores.update(process.result()[1])

    # write predicted truncation idxs to json
    out_path = "/playpen-storage/levlevi/contextualized-shot-quality-analysis/shot-quality-estimation/extract_shots/testing/data/B1_preds.json"
    json_object = json.dumps(preds, indent=4)
    with open(out_path, "w") as outfile:
        outfile.write(json_object)

    # write predicted conf scores to json
    conf_scores_out_path = "/playpen-storage/levlevi/contextualized-shot-quality-analysis/shot-quality-estimation/extract_shots/testing/data/B1_conf_scores.json"
    json_object = json.dumps(conf_scores, indent=4)
    with open(conf_scores_out_path, "w") as outfile:
        outfile.write(json_object)


if __name__ == "__main__":
    test_dir = "/playpen-storage/levlevi/contextualized-shot-quality-analysis/shot-quality-estimation/extract_shots/testing/data/nba_uncut_300_7s"
    predict_timestamps_dir(test_dir, max_processes=8)
