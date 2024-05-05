# **Ablation:** Jitter Scales

---

## **Setting**

| Model | Checkpoint | League | Train Set | Test Set | Shot-Result | Train Clips | Val Clips | Test Clips |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| TimeSFormer | Kinetics-600 | NBA 15-16 | Balanced | Imbalanced | Hidden | 4500 | 500 | 500 |

| Train Crop Size | # Epochs | # Frames | Sample-Rate | OG Video Res | Train Batch Size (Per Device) | Train Batch Size (Total) | Clip-Duration (Sec) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 224 | 10 | 60 | 2 | 853 x 480 | 3 | 28 |  4 |

| Test Batch Size (Total) | Test Crop Size | # Ensemble Views | 
| :---: | :---: | :---: |
| 64 | 224 | 1 |

| Condition | % Made | % Missed |
|:---: | :---: | :---: |
| Balanced | 50.00 | 50.00 |
| Imbalanced | 45.29 | 54.71 |

---

## **Experiments**

| Jitter Scales | Train Err | Train Loss | Val Err | Test Acc | Test Acc - Maj Cls |
| :---: | :---: | :---: | :---: | :---: | :---: |
| [224, 224] | 38.122 | 0.648 | 46.991 | 52.10 | --- | 
| [224, 256] | --- | --- | --- | --- | --- | 
| [224, 320] | --- | --- | --- | --- | --- | 
| [224, 398] | 41.828 | 0.675 | 48.172 |  49.10 | --- | 