# **Ablation:** Test Spatial Crops

## **Setting**

| model | checkpoint | league | train set | test set | shot-result| train clips | val clips | test clips |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
TimeSFormer | Kinetics-600 | NBA 15-16 | balanced | imbalanced | hidden | 4500 | 500 | 500 |

| train epochs | train crop size | # frames | sample-rate | train jitter scales | train batch size (per device) | clip-duration (sec) |
:---: | :---: | :---: | :---: | :---: | :---: | :---: |
20 | 224 | 60 | 2 | [224, 256] |  3 | 4 | 

| test batch size (total) | test crop size | # ensemble views | 
|:---: | :---: | :---: |
| 20 | 224 | 1 |


| condition | % made | % missed |
|:---: | :---: | :---: |
| balanced | 50.00 | 50.00 |
| imbalanced | 45.29 | 54.71 |

## **Experiments**

| # Spatial Crops | Test Acc | Test Acc - Maj Cls |
| :---: | :---: | :---: |
| 1 | 53.71 | --- |
| 2 | 53.31 | --- |
| 3 | **54.71** | --- |

# **Ablation:** Test Ensemble Views

## **Setting**

| model | checkpoint | league | train set | test set | shot-result| train clips | val clips | test clips |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
TimeSFormer | Kinetics-600 | NBA 15-16 | balanced | imbalanced | hidden | 4500 | 500 | 500 |

| train epochs | train crop size | # frames | sample-rate | train jitter scales | train batch size (per device) | clip-duration (sec) |
:---: | :---: | :---: | :---: | :---: | :---: | :---: |
20 | 224 | 60 | 2 | [224, 256] |  3 | 4 | 

| test batch size (total) | test crop size | # spatial crops | 
|:---: | :---: | :---: |
| 20 | 224 | 1 |


| condition | % made | % missed |
|:---: | :---: | :---: |
| balanced | 50.00 | 50.00 |
| imbalanced | 45.29 | 54.71 |

## **Experiments**

| # Ensemble Views | Ensemble Method | Test Acc | Test Acc - Maj Cls |
| :---: | :---: | :---: | :---: |
| 1 | sum |  **54.71** | **0.0** |
| 2 | sum | 54.71 | 0.0 |
| 2 | max | 54.31 | -0.4 |
| 3 | sum | 54.51 | -0.2 |
| 3 | max | 54.31 | -0.4 |
| 4 | sum | 54.71 | 0.0 |
| 4 | max | 54.31 | -0.4 |
| 5 | sum | 54.71 | 0.0 |
| 5 | max | 54.31 | -0.4 |