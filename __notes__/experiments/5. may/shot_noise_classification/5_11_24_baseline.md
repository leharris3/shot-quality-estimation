# **Ablation:** Baseline

---

## **Setting**

#### Model

| Model | Checkpoint |
| :---: | :---: |
| TimeSFormer | NBA-Result-Hidden-Large-Scale-50K | 

#### Data

| League | Train Set | Test Set | Shot-Result | Train Clips | Test Clips
 :---: | :---: | :---: | :---: | :---: | :---: |
| NBA 15-16 | Balanced | Balanced | Hidden | 2550 | 150

#### Train Config

| Train Crop Size | # Epochs | # Frames | Sample-Rate | OG Video Res | Jitter | Train Batch Size (Total) | Clip-Duration (Sec) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 224 | 20 | 32 | 1 | 853 x 480 | [224, 256] | 40 |  ~1s |

#### Test Config

| Test Crop Size | # Ensemble Views | # Spatial Crops | Test Batch Size (Total) |
| :---: | :---: | :---: | :---: |
| 224 | 1 | 3 | 8 |

---

## Experiments

| Train Err | Train Loss | Val Err |
| :---: | :---: | :---: |
| --- | --- | --- |