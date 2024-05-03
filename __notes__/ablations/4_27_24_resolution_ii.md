# ***ablation:*** clip resolution ii

## **Setting**

| model | checkpoint | league | train set | test set | shot-result| train clips | val clips | test clips | coverage | 
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
TimeSFormer | Kinetics-600 | NBA 15-16 | balanced | imbalanced | hidden | 4500 | 500 | 500 | 100%

| epochs| batch size (device) | clip-duration (sec) | jitter width-height ratio |
| :---: | :---: | :---: | :---: | 
20 | 2.5 | 4 | $256/224$ ~ 1.142

| condition | % made | % missed |
| --- | :---: | :---:|
| Balanced | 50.00 | 50.00 |
| Imbalanced | 44.65 | 55.35 |

## **Experiments**

| resolution | train err | train loss | val err | test acc | test acc - maj cls|
| :---: | :---: | :---: | :---: | :---: | :---: | 
| 224 x 224 | --- | --- | --- | --- |  --- | 
| 256 x 256 | --- | --- | --- | --- |  --- | 
| 320 x 320 | --- | --- | --- | --- |  --- | 
| 384 x 384 | --- | --- | --- | --- |  --- | 