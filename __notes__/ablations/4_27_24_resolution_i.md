# ***ablation:*** clip resolution i

## **Setting**

| model | checkpoint | league | train set | test set | shot-result | train clips | val clips | test clips | coverage | 
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
TimeSFormer | Kinetics-600 | NBA 15-16 | balanced | imbalanced | hidden | 900 | 100 | 500 | 100%

| epochs| batch size (device) | clip-duration (sec) | jitter width-height ratio |
| :---: | :---: | :---: | :---: | 
20 | 2.5 | 4 | $256/224$ ~ 1.142

## **Experiments**

| resolution | train err | train loss | val err | test acc | test acc - maj cls|
| :---: | :---: | :---: | :---: | :---: | :---: | 
| 224 x 224 | 27.976 | 0.555 | 43.670 | 54.11 |  --- | 
| 256 x 256 | 32.181 | 0.598 | 43.542 | 53.91 | --- |
| 320 x 320 | 30.280 | 0.581 | **42.731** | **54.90** | --- | 
| 384 x 384 | 30.7196 | 0.5896 | 45.054 | 52.30 | --- |