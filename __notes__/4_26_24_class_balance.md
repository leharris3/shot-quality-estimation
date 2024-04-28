# ***ablation:*** class balance

### **Setting**

| model | checkpoint | league | shot-result| train clips | val clips | test clips  
| --- | --- | --- | --- | --- | --- | --- | 
TimeSFormer | Kinetics-600 | NBA 15-16 | hidden | 4500 | 500 | 500 |

| epochs | input shape | train jitter scales | batch size (device) | clip-duration (sec) |
| --- | --- | --- | --- | --- |
|20 | 60 x 224 x 224 | [224, 256] | 2.5 | 4

| condition | % made | % missed |
| --- | --- | --- |
| Balanced | 50.00 | 50.00 |
| Imbalanced | 45.29 | 54.71 |

### **Experiments**

| train set | test set | train err | train loss | val err | test acc | test acc - maj cls|
| --- | --- | --- | :---: | --- | --- |  --- |
| Balanced | Balanced |  33.73 | 0.607 | 47.46 | 52.40 | **2.40** | 
| Balanced | Imbalanced | 33.73 | 0.607 | 47.46 | **57.11** | **2.40** |
| Imbalanced | Balanced | 28.87 | 0.564 | 45.96 | 49.00 | -1.00 |
| Imbalanced | Imbalanced | 28.87 | 0.564 | 45.96 | 54.51 | -0.20 |