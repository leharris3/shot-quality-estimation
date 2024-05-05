# **Ablation:** Batch Size

---

## **Setting**

| Model | Checkpoint | League | Train Set | Test Set | Shot-Result| Train Clips | Val Clips | Test Clips |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
TimeSFormer | Kinetics-600 | NBA 15-16 | Balanced | Balanced | hidden | 4500 | 500 | 500 |

| Epochs | Input Res | # Frames | Sample-Rate | Train Jitter | Batch Size (Per Device) | Clip-Duration (Sec) |
:---: | :---: | :---: | :---: | :---: | :---: | :---: |
20 | 224 x 224 | 60 | 2 | [224, 256] |  2.5 | 4 | 

---

## **Experiments**

| # Batch Size | Train Err | Train Loss | Val Err | Test Acc | Test Acc - Maj Cls|
| :---: | :---: | :---: | :---: | :---: | :---: | 
| 20 | 31.888 | 0.591 | 45.371 | 53.20 | 3.20 |
| 24 | 31.574 | 0.586 | **44.492** | 53.20 | 3.20 |
| 28 | 31.329 | 0.586 | 44.928 | 53.20 | 3.20 |
| 32 | OOM | OOM | OOM | OOM | OOM | OOM |