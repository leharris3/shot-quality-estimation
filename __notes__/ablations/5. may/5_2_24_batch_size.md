# **Ablation:** Batch Size

---

## **Setting**

| model | checkpoint | league | train set | test set | shot-result| train clips | val clips | test clips |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
TimeSFormer | Kinetics-600 | NBA 15-16 | balanced | imbalanced | hidden | 4500 | 500 | 500 |

| epochs | input res | # frames | sample-rate | train jitter scales | batch size (per device) | clip-duration (sec) |
:---: | :---: | :---: | :---: | :---: | :---: | :---: |
20 | 224 x 224 | 60 | 2 | [224, 256] |  2.5 | 4 | 

| condition | % made | % missed |
|:---: | :---: | :---: |
| balanced | 50.00 | 50.00 |
| imbalanced | 45.29 | 54.71 |

---

## **Experiments**

| # batch size | train err | train loss | val err | test acc | test acc - maj cls|
| :---: | :---: | :---: | :---: | :---: | :---: | 
| 20 | 31.888 | 0.591 | 45.371 | **55.71** | **1.0** |
| 24 | 31.574 | 0.586 | 44.492 | 54.71 | 0.0 |
| 28 | 31.329 | 0.586 | 44.928 | 54.11 | -0.6 |
| 32 | OOM | OOM | OOM | OOM | OOM | OOM |