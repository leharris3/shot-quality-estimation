# **Ablation:** # Frames

---

## **Setting**

| Model | Checkpoint | League | Train Set | Test Set | Shot-Result | Train Clips | Val Clips | Test Clips |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
TimeSFormer | Kinetics-600 | NBA 15-16 | Balanced | Balanced | Hidden | 4500 | 500 | 1300 |

| epochs | input res | train jitter scales | batch size (per device) | clip-duration (sec) |
:---: | :---: | :---: | :---: | :---: |
20 | 224 x 224 | [224, 256] |  2.5 | 4 | 

| condition | % made | % missed |
|:---: | :---: | :---: |
| balanced | 50.00 | 50.00 |
| imbalanced | 45.29 | 54.71 |

---

## **Experiments**

| # Frames x Sample Rate | Train Err | Train Loss | Val Err | Test Acc | Test Acc - Maj Cls|
| :---: | :---: | :---: | :---: | :---: | :---: |
| 8 x 15 | 35.456 | 0.620 | 44.170 | 52.15 | 2.15 | 
| **15 x 8** | 33.167 | 0.604 | 44.797 | **53.77** | **3.77** | 
| 30 x 4 | 32.748 | 0.588 | 45.940 | 51.85 | 1.85 | 
| 40 x 3 | 31.169 | 0.584 | 45.828 | 51.54 | 1.54 | 
| 60 x 2 | 31.888 | 0.591 | 45.371 | 52.46 | 2.46 | 
| 120 x 1 | OOM | OOM | OOM | OOM | OOM | 