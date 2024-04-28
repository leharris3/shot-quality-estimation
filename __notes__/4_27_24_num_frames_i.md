# ***ablation:*** # frames i

## **Setting**

| model | checkpoint | league | train set | test set | shot-result| train clips | val clips | test clips | coverage | 
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
TimeSFormer | Kinetics-600 | NBA 15-16 | balanced | imbalanced | hidden | 900 | 100 | 500 | 100%

| epochs | input res | train jitter scales | batch size (per device) | clip-duration (sec) |
:---: | :---: | :---: | :---: | :---: |
20 | 224 x 224 | [224, 256] |  2.5 | 4 | 

| condition | % made | % missed |
|:---: | :---: | :---: |
| balanced | 50.00 | 50.00 |
| imbalanced | 45.29 | 54.71 |

## **Experiments**

| # frames | train err | train loss | val err | test acc | test acc - maj cls|
| :---: | :---: | :---: | :---: | :---: | :---: | 
| 15 | 24.284 | 0.481 | 45.677 | 53.51 | -1.2 |
| 30 | 21.080 | 0.445 | **43.530** | **55.11** | **0.4** |
| 40 | 19.799 | 0.437 | 44.096 | 53.71 | -1 |
| 60 | 20.205 | 0.435  | 43.778 | 53.91 | -.8  |
| 120 | OOM | OOM | OOM | OOM | OOM |