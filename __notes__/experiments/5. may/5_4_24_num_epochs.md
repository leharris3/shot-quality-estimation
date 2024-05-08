# **Ablation:** Num Epochs

---

## **Setting**

| model | checkpoint | league | train set | test set | shot-result| train clips | val clips | test clips |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
TimeSFormer | Kinetics-600 | NBA 15-16 | balanced | imbalanced | hidden | 4500 | 500 | 500 |

| train crop size | # frames | sample-rate | train jitter scales | train batch size (per device) | clip-duration (sec) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 224 | 60 | 2 | [224, 256] | 3 | 4 | 

| test batch size (total) | test crop size | # ensemble views | 
|:---: | :---: | :---: |
| 20 | 224 | 1 |

| condition | % made | % missed |
|:---: | :---: | :---: |
| balanced | 50.00 | 50.00 |
| imbalanced | 45.29 | 54.71 |

---

## **Experiments**

| # Epochs | Test Acc | Test Acc - Maj Cls |
| :---: | :---: | :---: |
| 5 | 53.71 | -1.0 |
| 10 | 54.11 | -0.6 |
| 15 | 54.31 | -0.4 |
| 20 | **54.91** | **0.2** |