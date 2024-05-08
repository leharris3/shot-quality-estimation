# **Experiment:** NBA 50K

---

## **Setting**

#### Model

| Model | Checkpoint |
| :---: | :---: |
| TimeSFormer | Yulu 20-League Multi-Class | 

#### Data

| League | Train Set | Test Set | Shot-Result | Train Clips | Val Clips | Test Clips |
 :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| NBA 15-16 | Balanced | Balanced | Hidden | 45000 | 5000 | 500 |

#### Train Config

| Train Crop Size | # Epochs | # Frames | Sample-Rate | OG Video Res | Jitter | Train Batch Size (Total) | Clip-Duration (Sec) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 224 | 50 | 15 | 8 | 853 x 480 | [224, 256] | 28 |  4 |

#### Test Config

| Test Crop Size | # Ensemble Views | # Spatial Crops | Test Batch Size (Total) |
| :---: | :---: | :---: | :---: |
| 224 | 1 | 3 | 128 |

---

# Results

| # Test Samples | Test Games OOD? | Manually Reviewed? | Test Acc | Test Acc - Maj Cls  | 
| :---: | :---: | :---: | :---: | :---: |
| 500 | :white_check_mark: | :white_check_mark: | 53.60 | 3.60 |
| 1300 | :white_check_mark: | :x: | 55.77 | 5.77 |
| 1300 | :white_check_mark: | :white_check_mark: | 54.07 | 4.07 |