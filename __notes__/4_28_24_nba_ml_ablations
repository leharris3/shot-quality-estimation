# ***ablation:*** features

## **Setting**

model | league | train set | test set | shot-result| train samples | test samples |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| logisitic regression|  NBA 15-16 | imbalanced | imbalanced | hidden | 9000 | 1000 |

| condition | % made | % missed |
| --- | --- | --- |
| Balanced | 50.00 | 50.00 |
| Imbalanced | 44.65 | 55.35 |
##### CHANGE THESE VALS

## Experiments

| test acc | test acc - maj cls|  `attempt_type` | `player_id` | `team_id` | `period`| `pos_x`| `pos_y` |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |  :---: |
| 54.60 | 0.00 | :white_check_mark: | --- | --- | --- | --- | --- | --- | 
| 54.60 | 0.00 | :white_check_mark: | :white_check_mark: | --- | --- | --- | --- | --- |  
| 55.90 | 1.30 | :white_check_mark: | --- | :white_check_mark: | --- | --- | --- | --- | 
| 55.90 | 1.30 | :white_check_mark: | --- | :white_check_mark: | :white_check_mark: | --- | --- |
| 57.20 | 2.60 | :white_check_mark: | --- | :white_check_mark: | --- | :white_check_mark: | --- |
| 57.80 | 3.20 | :white_check_mark: | --- | :white_check_mark: | --- | :white_check_mark: | :white_check_mark:|
| 58.00 | 3.40 |:white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark:|
| 58.20 | 3.60 | :white_check_mark: | --- | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark:|
| **58.50** | **3.90** | :white_check_mark: | --- | :white_check_mark: | :white_check_mark: | :white_check_mark: | --- |

# ***ablation:*** class balance

model | league | shot-result| train samples | test samples |
| :---: | :---: | :---: | :---: | :---: |
| logisitic regression|  NBA 15-16 | hidden | 9000 | 1000 |

| condition | % made | % missed |
| --- | --- | --- |
| Balanced | 50.00 | 50.00 |
| Imbalanced | 44.65 | 55.35 |

| train set | test set | test acc |  test acc - maj cls |
| :---: | :---: | :---: | :---: |
| balanced | balanced | 55.00 | 5.00 |  
| balanced | imbalanced | 54.30 | -1.05 |  
| imbalanced | balanced | **57.90** | **7.90** |  
| imbalanced | imbalanced | 56.65 | 1.30 |  
