# **Ablation:** Features

## **Setting**

model | league | train set | test set | shot-result| train samples | test samples |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Logisitic Regression|  NBA 15-16 | imbalanced | imbalanced | hidden | 9000 | 1000 |

| condition | % made | % missed |
| --- | :---: | :---:|
| Balanced | 50.00 | 50.00 |
| Imbalanced | 44.65 | 55.35 |

## Experiments

| test acc | test acc - maj cls|  `attempt_type` | `player_id` | `team_id` | `period`| `pos_x`| `pos_y` |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |  :---: |
| 54.60 | -0.75 | :white_check_mark: | --- | --- | --- | --- | --- | --- | 
| 54.60 |  -0.75 | :white_check_mark: | :white_check_mark: | --- | --- | --- | --- | --- |  
| 55.90 | 0.55 | :white_check_mark: | --- | :white_check_mark: | --- | --- | --- | --- | 
| 55.90 | 0.55 | :white_check_mark: | --- | :white_check_mark: | :white_check_mark: | --- | --- |
| 57.20 | 1.85 | :white_check_mark: | --- | :white_check_mark: | --- | :white_check_mark: | --- |
| 57.80 | 2.45 | :white_check_mark: | --- | :white_check_mark: | --- | :white_check_mark: | :white_check_mark:|
| 58.00 | 2.65 |:white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark:|
| 58.20 | 2.85 | :white_check_mark: | --- | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark:|
| **58.50** | **3.15** | :white_check_mark: | --- | :white_check_mark: | :white_check_mark: | :white_check_mark: | --- |

# **Ablation:** Class Balance

model | league | shot-result| train samples | test samples |
| :---: | :---: | :---: | :---: | :---: |
| Logisitic Regression|  NBA 15-16 | hidden | 9000 | 1000 |

| condition | % made | % missed |
| --- | :---: | :---:|
| Balanced | 50.00 | 50.00 |
| Imbalanced | 44.65 | 55.35 |


## Experiments

| train set | test set | test acc |  test acc - maj cls |
| :---: | :---: | :---: | :---: |
| balanced | balanced | 53.10 | 3.10 |  
| balanced | imbalanced | 58.60 | 3.25 |  
| imbalanced | balanced | 53.10 | 3.10 |  
| imbalanced | imbalanced | **59.30** | **3.95** |  

# **Ablation:** Model Variants

| league | shot-result| train samples | test samples | train-set | test-set |
| :---: | :---: | :---: | :---: | :---: | :---: |
|  NBA 15-16 | hidden | 9000 | 1000 | imbalanced | balanced |

| condition | % made | % missed |
| --- | :---: | :---:|
| Balanced | 50.00 | 50.00 |
| Imbalanced | 44.65 | 55.35 |


## Experiments

| model | test acc |  test acc - maj cls |
| :--- | :---: | :---: |
| Logisitic Regression | 57.90 | 2.50 |
| Ridge Classifier | 59.20 | 3.85 |
| AdaBoost | 59.60 | 4.25 |
| Gradient Boosting | **61.60** | **6.25** |