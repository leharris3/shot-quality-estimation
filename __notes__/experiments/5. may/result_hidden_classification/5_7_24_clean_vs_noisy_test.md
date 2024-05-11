# **Ablation:** Performance on Different Test Sets

---

## **Setting**

#### Model

| Model | Checkpoint |
| :---: | :---: |
| TimeSFormer | Kinetics-600 | 

#### Data

| League | Train Set | Test Set | Shot-Result | Train Clips |
 :---: | :---: | :---: | :---: | :---: |
| NBA 15-16 | Balanced | Balanced | Hidden | 4500 |

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

| # Test Samples | Test Games OOD? | Manually Reviewed? | Test Acc | Test Acc - Maj Cls  | 
| :---: | :---: | :---: | :---: | :---: |
| 500 | :white_check_mark: | :white_check_mark: | 52.40 | 2.40 |
| 1300 | :white_check_mark: | :x: | 53.07 | 3.07 |
| 1300 | :white_check_mark: | :white_check_mark: | 52.46 | 2.46 |