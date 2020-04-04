======================================= Beginning of report ========================================



This following report is created by gordonchen on Apr,04 2020



================ Table Statistics ================

|                  |   count |
|:-----------------|--------:|
| n_row            |     891 |
| n_col            |      12 |
| n_missing_cell   |     866 |
| n_empty_row      |       0 |
| n_duplicated_row |       0 |
| n_Useless_var    |       2 |
| n_Binary_var     |       2 |
| n_Interval_var   |       5 |
| n_Nominal_var    |       3 |





================ Variable Summary ================

|             | type     | data_type   |   count |   n_missing | p_missing   |   n_unique | p_unique   |
|:------------|:---------|:------------|--------:|------------:|:------------|-----------:|:-----------|
| PassengerId | Useless  | Unique      |     891 |           0 | 0.00%       |        891 | 100.00%    |
| Name        | Useless  | Unique      |     891 |           0 | 0.00%       |        891 | 100.00%    |
| Survived    | Binary   | Numerical   |     891 |           0 | 0.00%       |          2 | 0.22%      |
| Sex         | Binary   | Categorical |     891 |           0 | 0.00%       |          2 | 0.22%      |
| Pclass      | Interval | Numerical   |     891 |           0 | 0.00%       |          3 | 0.34%      |
| Age         | Interval | Numerical   |     891 |         177 | 19.87%      |         88 | 12.32%     |
| SibSp       | Interval | Numerical   |     891 |           0 | 0.00%       |          7 | 0.79%      |
| Parch       | Interval | Numerical   |     891 |           0 | 0.00%       |          7 | 0.79%      |
| Fare        | Interval | Numerical   |     891 |           0 | 0.00%       |        248 | 27.83%     |
| Ticket      | Nominal  | Categorical |     891 |           0 | 0.00%       |        681 | 76.43%     |
| Cabin       | Nominal  | Categorical |     891 |         687 | 77.10%      |        147 | 72.06%     |
| Embarked    | Nominal  | Categorical |     891 |           2 | 0.22%       |          3 | 0.34%      |





============== Variable Statistics ===============



Useless variables:

|           | PassengerId   | Name    |
|:----------|:--------------|:--------|
| count     | 891           | 891     |
| n_missing | 0             | 0       |
| p_missing | 0.00%         | 0.00%   |
| n_unique  | 891           | 891     |
| p_unique  | 100.00%       | 100.00% |



Binary variables:

|           | Survived   | Sex    |
|:----------|:-----------|:-------|
| count     | 891        | 891    |
| n_missing | 0          | 0      |
| p_missing | 0.00%      | 0.00%  |
| n_unique  | 2          | 2      |
| p_unique  | 0.22%      | 0.22%  |
| value1    | 0          | male   |
| n_value1  | 549        | 577    |
| p_value1  | 61.62%     | 64.76% |
| value2    | 1          | female |
| n_value2  | 342        | 314    |
| p_value2  | 38.38%     | 35.24% |



Interval variables:

|              | Pclass   | Age      | SibSp   | Parch   | Fare       |
|:-------------|:---------|:---------|:--------|:--------|:-----------|
| count        | 891      | 891      | 891     | 891     | 891        |
| n_missing    | 0        | 177      | 0       | 0       | 0          |
| p_missing    | 0.00%    | 19.87%   | 0.00%   | 0.00%   | 0.00%      |
| n_unique     | 3        | 88       | 7       | 7       | 248        |
| p_unique     | 0.34%    | 12.32%   | 0.79%   | 0.79%   | 27.83%     |
| mean         | 2.3086   | 29.6991  | 0.523   | 0.3816  | 32.2042    |
| std          | 0.8361   | 14.5265  | 1.1027  | 0.8061  | 49.6934    |
| variance     | 0.699    | 211.0191 | 1.216   | 0.6497  | 2469.4368  |
| min          | 1.0      | 0.42     | 0.0     | 0.0     | 0.0        |
| 5%           | 1.0      | 4.0      | 0.0     | 0.0     | 7.225      |
| 25%          | 2.0      | 20.125   | 0.0     | 0.0     | 7.9104     |
| 50%          | 3.0      | 28.0     | 0.0     | 0.0     | 14.4542    |
| 75%          | 3.0      | 38.0     | 1.0     | 0.0     | 31.0       |
| 95%          | 3.0      | 56.0     | 3.0     | 2.0     | 112.0792   |
| max          | 3.0      | 80.0     | 8.0     | 6.0     | 512.3292   |
| range        | 2.0      | 79.58    | 8.0     | 6.0     | 512.3292   |
| iqr          | 1.0      | 17.875   | 1.0     | 0.0     | 23.0896    |
| kurtosis     | -1.28    | 0.1783   | 17.8804 | 9.7781  | 33.3981    |
| skewness     | -0.6305  | 0.3891   | 3.6954  | 2.7491  | 4.7873     |
| sum          | 2057.0   | 21205.17 | 466.0   | 340.0   | 28693.9493 |
| mean_abs_dev | 0.762    | 11.3229  | 0.7138  | 0.5807  | 28.1637    |
| coff_of_var  | 0.3621   | 0.4891   | 2.1085  | 2.1123  | 1.5431     |
| n_zeros      | 0        | 0        | 608     | 678     | 15         |
| p_zeros      | 0.0      | 0.0      | 0.6824  | 0.7609  | 0.0168     |



Nominal variables:

|           | Ticket   | Cabin   | Embarked   |
|:----------|:---------|:--------|:-----------|
| count     | 891      | 891     | 891        |
| n_missing | 0        | 687     | 2          |
| p_missing | 0.00%    | 77.10%  | 0.22%      |
| n_unique  | 681      | 147     | 3          |
| p_unique  | 76.43%   | 72.06%  | 0.34%      |
| mode      | 1601     | B96 B98 | S          |
| mode_freq | 7        | 4       | 644        |





================ Confusion Matrix ================

row:Survived - col:Sex

|    |   female |   male |
|---:|---------:|-------:|
|  0 |       81 |    468 |
|  1 |      233 |    109 |

========================================== End of report ===========================================
