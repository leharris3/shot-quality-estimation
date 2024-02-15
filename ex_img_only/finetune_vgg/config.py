import os

BASE_PATH = 'ataset'

CLASSES = ['make', 'miss']
BATCH_SIZE = 32

TRAIN = 'train'
TEST = 'test'
VAL = 'val'

LABEL_ENCODER_PATH = os.path.sep.join(['output', 'le.cpickle'])
BASE_CSV_PATH = 'output'
MODEL_PATH = os.path.sep.join(['output', 'shot-est-vgg-ft.model'])
UNFROZEN_PLOT_PATH = os.path.sep.join(["output", "unfrozen.png"])
WARMUP_PLOT_PATH = os.path.sep.join(["output", "warmup.png"])