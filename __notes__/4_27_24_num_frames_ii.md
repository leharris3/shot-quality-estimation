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

| # frames | train err | train loss | val err | test acc | test acc - maj cls|
| :---: | :---: | :---: | :---: | :---: | :---: | 
| 15 | --- | --- | --- | --- | --- |
| 30 | --- | --- | --- | --- | --- | --- |
| 40 | --- | --- | --- | --- | --- | --- |
| 60 | --- | --- | --- | --- | --- | --- |
| 120 | OOM | OOM | OOM | OOM | OOM |