import argparse
import random
import ffmpeg
import torch
import os
import concurrent.futures

from tqdm import tqdm
from timesformer.models.vit import TimeSformer
from torchvision.io import read_video
from torchvision.transforms import Resize, Compose
from scipy.ndimage import gaussian_filter1d

NUM_FRAMES = 32
MIN_FRAMES = 32
CUDA_DEVICE = 0
MIN_CONF_THRESH = 0.17

MADE_SHOT_SUBDIR = "made"
MISSED_SHOT_SUBDIR = "missed"
GARBAGE_SUBDIR = "garbage"

CLIP_OFFSET = 15
CLIP_OFFSET_SECONDS = 0.5

VID_LEN_FRAMES = 32
STEP = 6
FPS = 30.0


def read_video_to_tensor_buffer(video_path: str, device: int):

    # video_tensor, _, _ = read_video(video_path, output_format="TCHW", pts_unit="sec")
    # video_tensor = video_tensor.float().div_(255.0)
    # transforms = Compose([Resize((224, 224))])
    # if torch.cuda.is_available():
    #     video_tensor = video_tensor.cuda(device)
    # resized_tensor = transforms(video_tensor)
    # resized_tensor = resized_tensor.permute(1, 0, 2, 3).unsqueeze(0)
    # return resized_tensor

    video_tensor, _, _ = read_video(video_path, output_format="TCHW", pts_unit="sec")
    video_tensor = video_tensor.float() / 255.0
    transforms = Compose(
        [
            Resize((224, 224)),
        ]
    )
    resized_and_normalized_tensor = transforms(video_tensor)
    resized_and_normalized_tensor = resized_and_normalized_tensor.permute(
        1, 0, 2, 3
    ).unsqueeze(0)
    return resized_and_normalized_tensor


def find_local_min(array, thresh=MIN_CONF_THRESH):
    min_val = 2
    min_index = 0
    for i in range(len(array)):
        if array[i] < min_val and array[i] < thresh:
            min_val = array[i]
            min_index = i
    return min_index


def find_local_max(array, thresh=MIN_CONF_THRESH):
    max_val = -1
    max_index = 0
    for i in range(len(array)):
        if array[i] > max_val and array[i] > thresh:
            max_val = array[i]
            max_index = i
    return max_index


def pred_conf_scores(video_tensor, device, model, step_size: int = STEP):

    video_tensor = video_tensor.to(device)
    confidence_scores = []
    timestamps = []
    frame_increment = list(video_tensor.size())[2] - VID_LEN_FRAMES

    half_vid_len = VID_LEN_FRAMES // 2
    fps_inv = 1 / FPS

    with torch.no_grad():
        for index in range(0, frame_increment, step_size):
            temp_video = video_tensor[:, :, index : index + VID_LEN_FRAMES, :, :]
            preds = model(temp_video)
            probs = torch.nn.functional.softmax(preds, dim=1)
            confidence_scores.append(probs)
            timestamps.append(fps_inv * (index + half_vid_len))
    return confidence_scores, timestamps


def get_highest_conf_idx(confidence_scores, sigma: int = 5):
    idv_confidence_scores = [tensor[0][0].item() for tensor in confidence_scores]
    conf_denoise = gaussian_filter1d(idv_confidence_scores, sigma=sigma)
    return find_local_min(conf_denoise)


def split_shot_attempt_clip(
    video_path: str, dst_dir: str, local_min_index=0, skip_garbage=False
):
    """
    Given a path to an UNTRIMMED shot-attempt clip,
    create a TRIMMED shot attempt @dst_dir.
    """

    subdir = ""
    if "+" in video_path:
        subdir = MADE_SHOT_SUBDIR
    elif "-" in video_path:
        subdir = MISSED_SHOT_SUBDIR
    if local_min_index <= MIN_FRAMES or local_min_index > 210 - 32:
        subdir = GARBAGE_SUBDIR

    # calculate split point in seconds
    split_point_time = (local_min_index / FPS) - CLIP_OFFSET_SECONDS
    name = os.path.basename(video_path)

    if skip_garbage and subdir == GARBAGE_SUBDIR:
        return
    else:
        dst_path = os.path.join(dst_dir, subdir, name)
        (
            ffmpeg.input(video_path, ss=0, t=split_point_time)
            .output(dst_path, codec="copy")
            .global_args("-loglevel", "error")
            .run()
        )


def is_skip_video(video_path, dst_dir):
    name = os.path.basename(video_path)
    for subdir in [MADE_SHOT_SUBDIR, MISSED_SHOT_SUBDIR, GARBAGE_SUBDIR]:
        outpath = os.path.join(dst_dir, subdir, name)
        if os.path.isfile(outpath):
            return True
    return False


def split_all_shots_in_arr(
    src_dir: str, dst_dir: str, start_idx: int, end_idx: int, device=0
):
    """
    Truncate all shots-clips in an arr of file paths 'video_fps'.
    save to 'dst_dir'.
    """

    model = get_model(device)
    all_video_fps = []
    for root, _, files in os.walk(src_dir):
        for file in files:
            if ".mp4" in file:
                fp = os.path.join(root, file)
                all_video_fps.append(fp)
    all_video_fps = all_video_fps[start_idx:end_idx]
    random.shuffle(all_video_fps)

    for fp in tqdm(
        all_video_fps,
        desc=f"Truncating shot-attempts on device {device}",
        total=len(all_video_fps),
    ):
        if is_skip_video(fp, dst_dir):
            continue

        video_tensor = read_video_to_tensor_buffer(fp)
        if video_tensor is None:
            continue

        (
            conf_scores,
            timestamps,
        ) = pred_conf_scores(video_tensor, device=device, model=model)
        max_idx = get_highest_conf_idx(conf_scores, timestamps)

        try:
            max_idx = int(timestamps[max_idx] * FPS)
            split_shot_attempt_clip(fp, dst_dir, local_min_index=max_idx)
        except:
            print(f"Error processing video at {fp}")


def process_dir(shot_attempts_dir: str, dst_dir: str, num_devices=1):
    """
    Process all videos in `base_dir` in paralell across `num_devices`.
    """

    all_video_fps = []
    for root, _, files in os.walk(shot_attempts_dir):
        for file in files:
            if ".mp4" in file:
                fp = os.path.join(root, file)
                all_video_fps.append(fp)
    random.shuffle(all_video_fps)

    videos_per_device = len(all_video_fps) // num_devices

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_devices) as executor:
        futures = []
        for i in range(num_devices):
            start_idx = i * len(all_video_fps)
            end_idx = start_idx + videos_per_device
            subset_fps = all_video_fps[start_idx:end_idx]

            model = get_model(i)
            future = executor.submit(
                split_all_shots_in_arr, subset_fps, dst_dir, device=i, model=model
            )
            futures.append(future)
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                raise Exception(e)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Process video files for shot attempts analysis."
    )
    parser.add_argument("--src_dir", type=str)
    parser.add_argument(
        "--dst_dir", type=str, help="Destination directory to save processed videos."
    )
    parser.add_argument("--start_idx", type=str)
    parser.add_argument("--end_idx", type=str)
    parser.add_argument("--device", type=str, default=0, help="CUDA device ID.")
    return parser.parse_args()


def get_model(
    model_path: str = "",
    device: int = 0,
):
    model = TimeSformer(
        img_size=224,
        num_classes=2,
        num_frames=NUM_FRAMES,
        attention_type="divided_space_time",
        pretrained_model=model_path,
    ).to(device)
    return model


def main():
    args = parse_args()
    src_dir = args.src_dir
    dst_dir = args.dst_dir
    start_idx = int(args.start_idx)
    end_idx = int(args.end_idx)
    device = int(args.device)
    split_all_shots_in_arr(
        src_dir,
        dst_dir,
        start_idx,
        end_idx,
        device=device,
    )


if __name__ == "__main__":
    main()
