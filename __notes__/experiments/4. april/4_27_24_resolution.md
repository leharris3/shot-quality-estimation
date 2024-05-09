# **Ablation:** Clip Resolution

---

## **Setting**

| Model | Checkpoint | League | Train Set | Test Set | Shot-Result | Train Clips | Val Clips | Test Clips |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
TimeSFormer | Kinetics-600 | NBA 15-16 | Balanced | Balanced | Hidden | 4500 | 500 | 500 |

| Epochs| # GPUs | Batch Size (Total) | # Frames | Sample Rate |  Clip-Duration (Sec) | Jitter Width-Height Ratio | Test Crop |
| :---: | :---: | :---: | :---: |  :---: |  :---: |  :---: | :---: | 
20 | 8 | 12 | 60 | 2 | 4 | $256/224$ ~ 1.142 | ~Train Crop ~ Height

| condition | % made | % missed |
|:---: | :---: | :---: |
| balanced | 50.00 | 50.00 |
| imbalanced | 45.29 | 54.71 |

---

## **Experiments**

| Resolution | Train Err | Train Loss | Val Err | Test Acc | Test Acc - Maj Cls|
| :---: | :---: | :---: | :---: | :---: | :---: | 
| **224 x 224** | 31.888 | 0.591 | 45.371 | **52.46** | **2.46** |
| 256 x 256 | 34.582 | 0.620 | 47.064 | 50.69 | 0.69 |
| 320 x 320 | 36.036 | 0.626 | 45.659 | 49.61 | -0.39 |
| 384 x 384 | 35.104 | 0.623 | 46.466 | 50.15 | 0.15 |