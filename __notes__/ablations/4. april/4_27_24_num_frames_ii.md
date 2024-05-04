# ***ablation:*** # frames ii

## **Setting**

| model | checkpoint | league | train set | test set | shot-result| train clips | val clips | test clips | coverage | 
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
TimeSFormer | Kinetics-600 | NBA 15-16 | balanced | imbalanced | hidden | 4500 | 500 | 500 | 100%

| epochs | input res | train jitter scales | batch size (per device) | clip-duration (sec) |
:---: | :---: | :---: | :---: | :---: |
20 | 224 x 224 | [224, 256] |  2.5 | 4 | 

| condition | % made | % missed |
|:---: | :---: | :---: |
| balanced | 50.00 | 50.00 |
| imbalanced | 45.29 | 54.71 |

## **Experiments**
train err | train loss | val err | test acc | test acc - maj cls|
| # frames | 
| :---: | :---: | :---: | :---: | :---: | :---: | 
| 15 | 33.167 | 0.604 | **44.797** | 53.51 | -1.20 |
| 30 | 32.748 | 0.588 | 45.940 | 52.10 | -2.61 |
| 40 | 31.169 | 0.584 | 45.828 | 52.30 | -2.41 | 
| 60 | 31.888 | 0.591 | 45.371 | **55.71** | **1.00** |
| 120 | OOM | OOM | OOM | OOM | OOM |