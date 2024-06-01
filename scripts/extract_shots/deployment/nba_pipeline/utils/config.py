MODEL_FP = "/playpen-storage/levlevi/contextualized-shot-quality-analysis/data/experiments/_timesformer_/__runs__/result-noise-cls/nba_result_cls_3k_32_frames_224/checkpoints/checkpoint_epoch_00020.pyth"

MADE_SHOT_SUBDIR = "made"
MISSED_SHOT_SUBDIR = "missed"
GARBAGE_SUBDIR = "garbage"

# duration of final truncated clip
OUT_SHOT_DURATION_SEC = 4

# final output video height, og aspect ratio maintained
TARGET_HEIGHT = 480

# duration of temp clip
TEMP_SHOT_DURATION_SEC = 7

# fps for original and truncated video
FPS = 30

# temp clip start time: timestamp (given by logs) - 5.0s
TEMP_SHOT_OFFSET_SEC = 5

# truncate original video 20 frames after max_conf timestamp
# optimal split deterimined by analysis done in the testing folder
OUT_SHOT_OFFSET_SEC = 20 / 30

# length of inputs processed by TimeSformer model
MODEL_NUM_FRAMES = 32

OUT_SHOT_OFFSET_NUM_FRAMES = 20
LOW_NOISE_IDX = 20
HIGH_NOISE_IDX = 210 - (120)

# total frame count of temp vid
TEMP_VID_NUM_FRAMES = int(TEMP_SHOT_DURATION_SEC * FPS)

STEP = 6
SIGMA = 4
NUM_GPUS = 8