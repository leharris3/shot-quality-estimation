import ffmpeg
import torch
import os

from timesformer.models.vit import TimeSformer
from torchvision.io import read_video
from torchvision.transforms import Resize
from scipy.ndimage import gaussian_filter1d
from utils.config import *

MADE_SHOT_SUBDIR = "made"
MISSED_SHOT_SUBDIR = "missed"
GARBAGE_SUBDIR = "garbage"


def read_video_to_tensor_buffer(video_path: str):
    video_tensor, _, _ = read_video(video_path, output_format="TCHW", pts_unit="sec")
    video_tensor = video_tensor.float().div_(255.0)
    transform = Resize((224, 224))
    video_tensor = transform(video_tensor)
    video_tensor = video_tensor.permute(1, 0, 2, 3).unsqueeze_(0)
    return video_tensor


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
    frame_increment = video_tensor.size(2) - MODEL_NUM_FRAMES
    half_vid_len = MODEL_NUM_FRAMES // 2
    fps_inv = 1 / FPS
    confidence_scores = []
    timestamps = []

    with torch.no_grad():
        for index in range(0, frame_increment, step_size):
            temp_video = video_tensor[:, :, index : index + MODEL_NUM_FRAMES, :, :]
            preds = model(temp_video)
            probs = torch.nn.functional.softmax(preds, dim=1)
            confidence_scores.append(probs)
            timestamps.append(fps_inv * (index + half_vid_len))
    
    return confidence_scores, timestamps


def get_highest_conf_idx(confidence_scores, sigma: int = SIGMA, min_conf_thresh=MIN_CONF_THRESH):
    idv_confidence_scores = [tensor.cpu()[0][0] for tensor in confidence_scores]
    conf_denoise = gaussian_filter1d(idv_confidence_scores, sigma=sigma)
    return find_local_max(conf_denoise, min_conf_thresh)


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
    if local_min_index <= LOW_NOISE_IDX or local_min_index > HIGH_NOISE_IDX:
        subdir = GARBAGE_SUBDIR

    split_point_time = (local_min_index / FPS) - OUT_SHOT_OFFSET_SEC
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


def get_model(
    model_path: str = "",
    device: int = 0,
):
    model = TimeSformer(
        img_size=224,
        num_classes=2,
        num_frames=MODEL_NUM_FRAMES,
        attention_type="divided_space_time",
        pretrained_model=model_path,
    ).to(device)
    return model

