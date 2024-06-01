import os
os.chdir("/playpen-storage/levlevi/contextualized-shot-quality-analysis/shot-quality-estimation/TimeSformer")

from pathlib import Path

import torch
from timesformer.models.vit import TimeSformer

model_file = Path("/playpen-storage/levlevi/contextualized-shot-quality-analysis/data/experiments/_timesformer_/__runs__/baselines/TimeSformer_divST_8x32_224_K600.pyth")
model_file.exists()

model = TimeSformer(img_size=224, num_classes=600, num_frames=8, attention_type='divided_space_time',  pretrained_model=str(model_file))

dummy_video = torch.randn(2, 3, 8, 224, 224) # (batch x channels x frames x height x width)

pred = model(dummy_video,) # (2, 600)

assert pred.shape == (2,600)