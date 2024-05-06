# **Ablation:** # Frames

---

## **Setting**

| Model | Checkpoint | League | Train Set | Test Set | Shot-Result | Train Clips | Val Clips | Test Clips |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
TimeSFormer | Kinetics-600 | NBA 15-16 | Balanced | Balanced | Hidden | 4500 | 500 | 500 |

| epochs | input res | train jitter scales | batch size (per device) | clip-duration (sec) |
:---: | :---: | :---: | :---: | :---: |
20 | 224 x 224 | [224, 256] |  2.5 | 4 | 

| condition | % made | % missed |
|:---: | :---: | :---: |
| balanced | 50.00 | 50.00 |
| imbalanced | 45.29 | 54.71 |

---

## **Experiments**

| # frames | train err | train loss | val err | test acc | test acc - maj cls|
| :---: | :---: | :---: | :---: | :---: | :---: |
| 8 | 35.456 | 0.620 | 44.17 | 54.20 | 4.20 | 
| 15 | 33.167 | 0.604 | 44.797 | **54.80**| **4.80** |
| 30 | 32.748 | 0.588 | 45.940 | 52.00 | 2.00 |
| 40 | 31.169 | 0.584 | 45.828 | 52.00 | 2.00 | 
| 60 | 31.888 | 0.591 | 45.371 | 54.60 | 4.60 |
| 120 | OOM | OOM | OOM | OOM | OOM |