# **Ablation:** Scale

---

## **Setting**

#### Model

| Model | Checkpoint |
| :---: | :---: |
| TimeSFormer | Yulu 20-League Multi-Class | 

#### Data

| League | Train Set | Test Set | Shot-Result | Train Clips | Val Clips | Test Clips |
 :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| NBA 15-16 | Balanced | Balanced | Hidden | 25500 | 3000 | 1300 |

#### Train Config

| Train Crop Size | # Epochs | # Frames | Sample-Rate | OG Video Res | Jitter | Train Batch Size (Total) | Clip-Duration (Sec) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 224 | 20 | 60 | 2 | 853 x 480 | [224, 256] | 28 |  4 |

#### Test Config

| Test Crop Size | # Ensemble Views | # Spatial Crops | Test Batch Size (Total) |
| :---: | :---: | :---: | :---: |
| 224 | 1 | 3 | 128 |

---

## **Experiments**

#### Data Quality

| Mean Diff (Frames)| % Result Shown | Clip Recall | Test Acc | Test Acc - Maj Cls |
| :---: | :---: | :---: | :---: | :---: |
| -70.864 | **3.78** | **0.704** | 54.384 | 4.384 |
| **-32.248** | 5.10 | 0.351 | --- | --- |