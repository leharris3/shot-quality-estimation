# **Ablation:** Checkpoints

---

## **Setting**

| Model | Checkpoint | League | Train Set | Test Set | Shot-Result | Train Clips | Val Clips | Test Clips |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| TimeSFormer | Kinetics-600 | NBA 15-16 | Balanced | Balanced | Hidden | 4500 | 500 | 1300 |

| Train Crop Size | # Epochs | # Frames | Sample-Rate | OG Video Res | Jitter | Train Batch Size (Per Device) | Train Batch Size (Total) | Clip-Duration (Sec) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 224 | 20 | 60 | 2 | 853 x 480 | [224, 256] | 3 | 28 |  4 |

| Test Batch Size (Total) | Test Crop Size | # Ensemble Views | 
| :---: | :---: | :---: |
| 64 | 224 | 1 |

---

## **Experiments**

| Checkpoint | Train Err | Train Loss | Val Err | Test Acc | Test Acc - Maj Cls |
| :---: | :---: | :---: | :---: | :---: | :---: |
| TimeSformer_divST_8x32_224_K600 | 31.888 | 0.591 | 45.371 | 52.46 | 2.46 |
| **Yulu 20-League Multi-Class** | 40.632 | 0.659 | 42.757 | **53.15** | **3.15** |