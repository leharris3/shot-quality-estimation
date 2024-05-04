# ***ablation:*** clip resolution ii

## **Setting**

| model | checkpoint | league | train set | test set | shot-result| train clips | val clips | test clips |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
TimeSFormer | Kinetics-600 | NBA 15-16 | balanced | imbalanced | hidden | 4500 | 500 | 500 |

| epochs| # gpus | batch size (total) | # frames | sample rate |  clip-duration (sec) | jitter width-height ratio |
| :---: | :---: | :---: | :---: |  :---: |  :---: |  :---: | 
20 | 8 | 1.5 | 60 | 2 | 4 | $256/224$ ~ 1.142

| condition | % made | % missed |
| --- | :---: | :---:|
| Balanced | 50.00 | 50.00 |
| Imbalanced | 44.65 | 55.35 |

## **Experiments**

| resolution | train err | train loss | val err | test acc | test acc - maj cls|
| :---: | :---: | :---: | :---: | :---: | :---: | 
| 224 x 224 | --- | --- | --- | --- |  --- | 
| 256 x 256 | --- | --- | --- | --- |  --- | 
| 320 x 320 | 37.523 | 0.626 | 44.444 | 52.10 |  --- | 
| 384 x 384 | --- | --- | --- | --- |  --- | 