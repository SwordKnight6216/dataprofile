================================== Beginning of report ===================================



This following report is created by Gordon Chen on Sunday, Sep 20, 2020



================ Table Statistics ================

|                  |   count |
|:-----------------|--------:|
| n_row            |     891 |
| n_col            |      12 |
| n_missing_cell   |     866 |
| n_empty_row      |       0 |
| n_duplicated_row |       0 |
| n_Useless_var    |       1 |
| n_Binary_var     |       2 |
| n_Interval_var   |       6 |
| n_Nominal_var    |       3 |





================ Variable Summary ================

|             | type     | data_type   |   count |   n_missing | p_missing   |   n_unique | p_unique   |
|:------------|:---------|:------------|--------:|------------:|:------------|-----------:|:-----------|
| Name        | ID       | Unique      |     891 |           0 | 0.00%       |        891 | 100.00%    |
| Sex         | Binary   | Categorical |     891 |           0 | 0.00%       |          2 | 0.22%      |
| Survived    | Binary   | Numerical   |     891 |           0 | 0.00%       |          2 | 0.22%      |
| Pclass      | Interval | Numerical   |     891 |           0 | 0.00%       |          3 | 0.34%      |
| PassengerId | Interval | Numerical   |     891 |           0 | 0.00%       |        891 | 100.00%    |
| SibSp       | Interval | Numerical   |     891 |           0 | 0.00%       |          7 | 0.79%      |
| Parch       | Interval | Numerical   |     891 |           0 | 0.00%       |          7 | 0.79%      |
| Age         | Interval | Numerical   |     891 |         177 | 19.87%      |         88 | 12.32%     |
| Fare        | Interval | Numerical   |     891 |           0 | 0.00%       |        248 | 27.83%     |
| Ticket      | Nominal  | Categorical |     891 |           0 | 0.00%       |        681 | 76.43%     |
| Cabin       | Nominal  | Categorical |     891 |         687 | 77.10%      |        147 | 72.06%     |
| Embarked    | Nominal  | Categorical |     891 |           2 | 0.22%       |          3 | 0.34%      |





============== Variable Statistics ===============



Useless variables:

|           | Name    |
|:----------|:--------|
| count     | 891     |
| n_missing | 0       |
| p_missing | 0.00%   |
| n_unique  | 891     |
| p_unique  | 100.00% |



Binary variables:

|           | Sex    | Survived   |
|:----------|:-------|:-----------|
| count     | 891    | 891        |
| n_missing | 0      | 0          |
| p_missing | 0.00%  | 0.00%      |
| n_unique  | 2      | 2          |
| p_unique  | 0.22%  | 0.22%      |
| value1    | male   | 0          |
| n_value1  | 577    | 549        |
| p_value1  | 64.76% | 61.62%     |
| value2    | female | 1          |
| n_value2  | 314    | 342        |
| p_value2  | 35.24% | 38.38%     |



Interval variables:

|              | Pclass   | PassengerId   | SibSp   | Parch   | Age         | Fare        |
|:-------------|:---------|:--------------|:--------|:--------|:------------|:------------|
| count        | 891      | 891           | 891     | 891     | 891         | 891         |
| n_missing    | 0        | 0             | 0       | 0       | 177         | 0           |
| p_missing    | 0.00%    | 0.00%         | 0.00%   | 0.00%   | 19.87%      | 0.00%       |
| n_unique     | 3        | 891           | 7       | 7       | 88          | 248         |
| p_unique     | 0.34%    | 100.00%       | 0.79%   | 0.79%   | 12.32%      | 27.83%      |
| mean         | 2.3086   | 446.0000      | 0.5230  | 0.3816  | 29.6991     | 32.2042     |
| std          | 0.8361   | 257.3538      | 1.1027  | 0.8061  | 14.5265     | 49.6934     |
| variance     | 0.6990   | 66,231.0000   | 1.2160  | 0.6497  | 211.0191    | 2,469.4368  |
| min          | 1        | 1             | 0       | 0       | 0.4200      | 0.0000      |
| 5%           | 1.0000   | 45.5000       | 0.0000  | 0.0000  | 4.0000      | 7.2250      |
| 25%          | 2.0000   | 223.5000      | 0.0000  | 0.0000  | 20.1250     | 7.9104      |
| 50%          | 3.0000   | 446.0000      | 0.0000  | 0.0000  | 28.0000     | 14.4542     |
| 75%          | 3.0000   | 668.5000      | 1.0000  | 0.0000  | 38.0000     | 31.0000     |
| 95%          | 3.0000   | 846.5000      | 3.0000  | 2.0000  | 56.0000     | 112.0791    |
| max          | 3        | 891           | 8       | 6       | 80.0000     | 512.3292    |
| range        | 2        | 890           | 8       | 6       | 79.5800     | 512.3292    |
| iqr          | 1.0000   | 445.0000      | 1.0000  | 0.0000  | 17.8750     | 23.0896     |
| kurtosis     | -1.2800  | -1.2000       | 17.8804 | 9.7781  | 0.1783      | 33.3981     |
| skewness     | -0.6305  | 0.0000        | 3.6954  | 2.7491  | 0.3891      | 4.7873      |
| sum          | 2,057    | 397,386       | 466     | 340     | 21,205.1700 | 28,693.9493 |
| mean_abs_dev | 0.7620   | 222.7497      | 0.7138  | 0.5807  | 11.3229     | 28.1637     |
| coff_of_var  | 0.3621   | 0.5770        | 2.1085  | 2.1123  | 0.4891      | 1.5431      |
| n_zeros      | 0        | 0             | 608     | 678     | 0           | 15          |
| p_zeros      | 0.0000   | 0.0000        | 0.6824  | 0.7609  | 0.0000      | 0.0168      |



Nominal variables:

|                | Ticket   | Cabin       | Embarked   |
|:---------------|:---------|:------------|:-----------|
| count          | 891      | 891         | 891        |
| n_missing      | 0        | 687         | 2          |
| p_missing      | 0.00%    | 77.10%      | 0.22%      |
| n_unique       | 681      | 147         | 3          |
| p_unique       | 76.43%   | 72.06%      | 0.34%      |
| mode           | CA. 2343 | G6          | S          |
| mode_freq      | 7        | 4           | 644        |
| 2nd_freq_value | 1601     | C23 C25 C27 | C          |
| 2nd_freq       | 7        | 4           | 168        |
| 3rd_freq_value | 347082   | B96 B98     | Q          |
| 3rd_freq       | 7        | 4           | 77         |





================ Confusion Matrix ================

row:Sex - col:Survived

|        |   0 |   1 |
|:-------|----:|----:|
| female |  81 | 233 |
| male   | 468 | 109 |

===================================== End of report ======================================

============ Author of Dataprofile: Gordon Chen (GordonChen.GoBlue@gmail.com) ============
