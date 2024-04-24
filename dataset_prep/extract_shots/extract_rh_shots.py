from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from extract_rs_shots import *
from truncate_clips_helpers import (
    get_model,
    read_video_to_tensor_buffer,
    pred_conf_scores,
    get_highest_conf_idx,
)
from paths import LOCAL_DIR


MODEL_FP = (
    LOCAL_DIR
    + "contextualized-shot-quality-analysis/data/experiments/__runs__/result-noise-cls/nba_result_cls_3k_32_frames_224/checkpoints/checkpoint_epoch_00020.pyth"
)

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

STEP = 5
SIGMA = 9
THREADS = 1


def run_parallel_job(
    dst_dir: str, hudl_logs_dir: str, videos_dir: str, num_devices: int = 1
):

    log_fps = generate_file_paths(hudl_logs_dir)
    videos_fps = generate_file_paths(videos_dir)
    logs_vids_mapped = map_logs_to_videos(videos_fps, log_fps)
    num_vids_per_device = len(logs_vids_mapped) // num_devices

    with ProcessPoolExecutor(max_workers=num_devices) as executor:
        processes = []
        for device in range(num_devices):
            start_idx = device * num_vids_per_device
            end_idx = min(start_idx + num_vids_per_device, len(logs_vids_mapped))
            subset = logs_vids_mapped[start_idx:end_idx]
            process = executor.submit(
                extract_result_hidden_shots_from_map, dst_dir, subset, device
            )
            processes.append(process)
        for process in concurrent.futures.as_completed(processes):
            process.result()


def extract_result_hidden_shots_from_map(
    dst_dir: str, logs_vids_mapped, device: int = 0, num_workers=THREADS
):
    """
    Extracts uniform length shot-attempt clips with the shot-result hidden.
    """

    num_vids_per_worker = len(logs_vids_mapped) // num_workers
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        processes = []
        for worker in range(num_workers):
            start_idx = worker * num_vids_per_worker
            end_idx = min(start_idx + num_vids_per_worker, len(logs_vids_mapped))
            subset = logs_vids_mapped[start_idx:end_idx]

            model = get_model(device=device, model_path=MODEL_FP)
            process = executor.submit(_process_thread, dst_dir, subset, device, model)
            processes.append(process)
        for process in concurrent.futures.as_completed(processes):
            print(process.result())


def _process_thread(dst_dir: str, logs_vids_mapped, device: int = 0, model=None):

    for video_fp, log_fp in logs_vids_mapped:
        _process_video_log_pair_result_hidden(dst_dir, video_fp, log_fp, device, model)


def _process_video_log_pair_result_hidden(
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
    _extract_shots_result_hidden(
        dst_dir,
        shot_attempts,
        video_fp,
        device=device,
        timesformer_model=model,
    )


def _extract_shots_result_hidden(
    dst_dir: str,
    shot_attempts: pd.DataFrame,
    video_fp: str,
    device: int = 0,
    timesformer_model=None,
):
    """
    Extract all shots from `shot-attempts`, find moment of shot-release, and save a truncated
    shot attempts to `dst_dir`.

    Args:
        dst_dir (str): Directory where results will be saved.
        shot_attempts (DataFrame): DataFrame containing shot attempts data.
        video_fp (str): File path to the video file.s
        device (int, optional): Device ID for processing. Defaults to 0.
        model (optional): The model to use for processing video frames. Defaults to None.
    """

    period = int(video_fp.split("_period")[1].split(".mp4")[0])
    game_id = os.path.basename(video_fp).split("_")[0]
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

        # skip existing shots
        for subdir in [MADE_SHOT_SUBDIR, MISSED_SHOT_SUBDIR, GARBAGE_SUBDIR]:
            outpath = os.path.join(dst_dir, subdir, clip_name)
            if os.path.isfile(outpath):
                return

        start_time = row.second - TEMP_SHOT_OFFSET_SEC
        probe = ffmpeg.probe(video_fp)
        video_stream = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
            None,
        )

        if not video_stream:
            raise ValueError("No video stream found in the input file.")
        aspect_ratio = int(video_stream["width"]) / int(video_stream["height"])

        # 1. save a noisy shot-attempt clip
        save_shot_clip(
            video_fp,
            dst_path,
            start_time,
            TEMP_SHOT_DURATION_SEC,
            height=TARGET_HEIGHT,
            aspect_ratio=aspect_ratio,
        )

        video_tensor = read_video_to_tensor_buffer(dst_path, device=device)
        if video_tensor is None:
            continue

        # remove the noisy clip
        os.remove(dst_path)

        (
            conf_scores,
            timestamps,
        ) = pred_conf_scores(
            video_tensor, device=device, model=timesformer_model, step_size=STEP
        )
        max_idx = get_highest_conf_idx(conf_scores, sigma=2)
        # print(f"Max conf idx: {max_idx}")

        split_point_sec = timestamps[max_idx] - OUT_SHOT_OFFSET_SEC
        new_start_time = start_time + split_point_sec - OUT_SHOT_DURATION_SEC

        # print(f"Splitting at: {split_point_sec}")
        # print(f"New start time: {new_start_time}")

        adj_idx = STEP * max_idx
        subdir = ""
        if "+" in dst_path:
            subdir = MADE_SHOT_SUBDIR
        elif "-" in dst_path:
            subdir = MISSED_SHOT_SUBDIR
        if (
            adj_idx <= MODEL_NUM_FRAMES
            or adj_idx > TEMP_VID_NUM_FRAMES - MODEL_NUM_FRAMES
        ):
            subdir = GARBAGE_SUBDIR

        name = os.path.basename(dst_path)
        new_dst_path = os.path.join(dst_dir, subdir, name)

        try:
            # 2. save a corrected clip
            save_shot_clip(
                video_fp,
                new_dst_path,
                new_start_time,
                OUT_SHOT_DURATION_SEC,
                height=TARGET_HEIGHT,
                aspect_ratio=aspect_ratio,
            )
        except:
            print(f"Error processing video at {dst_path}")
            continue


def main():

    dst_dir = (
        LOCAL_DIR
        + "contextualized-shot-quality-analysis/data/experiments/result-hidden/nba_results_hidden_?k"
    )
    hudl_logs_dir = (
        LOCAL_DIR
        + "contextualized-shot-quality-analysis/data/nba/result-hidden-split/hudl-game-logs"
    )
    nba_replays_dir = (
        LOCAL_DIR
        + "contextualized-shot-quality-analysis/data/nba/result-hidden-split/replays"
    )

    run_parallel_job(dst_dir, hudl_logs_dir, nba_replays_dir, num_devices=8)


if __name__ == "__main__":
    main()
