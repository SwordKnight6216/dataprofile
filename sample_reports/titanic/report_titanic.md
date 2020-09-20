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
| n_Useless_var    |       2 |
| n_Binary_var     |       2 |
| n_Interval_var   |       5 |
| n_Nominal_var    |       3 |





================ Variable Summary ================

|             | type     | data_type   |   count |   n_missing | p_missing   |   n_unique | p_unique   |
|:------------|:---------|:------------|--------:|------------:|:------------|-----------:|:-----------|
| PassengerId | Useless  | Unique      |     891 |           0 | 0.00%       |        891 | 100.00%    |
| Name        | Useless  | Unique      |     891 |           0 | 0.00%       |        891 | 100.00%    |
| Sex         | Binary   | Categorical |     891 |           0 | 0.00%       |          2 | 0.22%      |
| Survived    | Binary   | Numerical   |     891 |           0 | 0.00%       |          2 | 0.22%      |
| Pclass      | Interval | Numerical   |     891 |           0 | 0.00%       |          3 | 0.34%      |
| Parch       | Interval | Numerical   |     891 |           0 | 0.00%       |          7 | 0.79%      |
| SibSp       | Interval | Numerical   |     891 |           0 | 0.00%       |          7 | 0.79%      |
| Fare        | Interval | Numerical   |     891 |           0 | 0.00%       |        248 | 27.83%     |
| Age         | Interval | Numerical   |     891 |         177 | 19.87%      |         88 | 12.32%     |
| Embarked    | Nominal  | Categorical |     891 |           2 | 0.22%       |          3 | 0.34%      |
| Ticket      | Nominal  | Categorical |     891 |           0 | 0.00%       |        681 | 76.43%     |
| Cabin       | Nominal  | Categorical |     891 |         687 | 77.10%      |        147 | 72.06%     |





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

|              | Pclass   | Parch   | SibSp   | Fare        | Age         |
|:-------------|:---------|:--------|:--------|:------------|:------------|
| count        | 891      | 891     | 891     | 891         | 891         |
| n_missing    | 0        | 0       | 0       | 0           | 177         |
| p_missing    | 0.00%    | 0.00%   | 0.00%   | 0.00%       | 19.87%      |
| n_unique     | 3        | 7       | 7       | 248         | 88          |
| p_unique     | 0.34%    | 0.79%   | 0.79%   | 27.83%      | 12.32%      |
| mean         | 2.3086   | 0.3816  | 0.5230  | 32.2042     | 29.6991     |
| std          | 0.8361   | 0.8061  | 1.1027  | 49.6934     | 14.5265     |
| variance     | 0.6990   | 0.6497  | 1.2160  | 2,469.4368  | 211.0191    |
| min          | 1        | 0       | 0       | 0.0000      | 0.4200      |
| 5%           | 1.0000   | 0.0000  | 0.0000  | 7.2250      | 4.0000      |
| 25%          | 2.0000   | 0.0000  | 0.0000  | 7.9104      | 20.1250     |
| 50%          | 3.0000   | 0.0000  | 0.0000  | 14.4542     | 28.0000     |
| 75%          | 3.0000   | 0.0000  | 1.0000  | 31.0000     | 38.0000     |
| 95%          | 3.0000   | 2.0000  | 3.0000  | 112.0791    | 56.0000     |
| max          | 3        | 6       | 8       | 512.3292    | 80.0000     |
| range        | 2        | 6       | 8       | 512.3292    | 79.5800     |
| iqr          | 1.0000   | 0.0000  | 1.0000  | 23.0896     | 17.8750     |
| kurtosis     | -1.2800  | 9.7781  | 17.8804 | 33.3981     | 0.1783      |
| skewness     | -0.6305  | 2.7491  | 3.6954  | 4.7873      | 0.3891      |
| sum          | 2,057    | 340     | 466     | 28,693.9493 | 21,205.1700 |
| mean_abs_dev | 0.7620   | 0.5807  | 0.7138  | 28.1637     | 11.3229     |
| coff_of_var  | 0.3621   | 2.1123  | 2.1085  | 1.5431      | 0.4891      |
| n_zeros      | 0        | 678     | 608     | 15          | 0           |
| p_zeros      | 0.0000   | 0.7609  | 0.6824  | 0.0168      | 0.0000      |



Nominal variables:

|                | Embarked   | Ticket   | Cabin       |
|:---------------|:-----------|:---------|:------------|
| count          | 891        | 891      | 891         |
| n_missing      | 2          | 0        | 687         |
| p_missing      | 0.22%      | 0.00%    | 77.10%      |
| n_unique       | 3          | 681      | 147         |
| p_unique       | 0.34%      | 76.43%   | 72.06%      |
| mode           | S          | CA. 2343 | C23 C25 C27 |
| mode_freq      | 644        | 7        | 4           |
| 2nd_freq_value | C          | 1601     | B96 B98     |
| 2nd_freq       | 168        | 7        | 4           |
| 3rd_freq_value | Q          | 347082   | G6          |
| 3rd_freq       | 77         | 7        | 4           |





================ Confusion Matrix ================

row:Sex - col:Survived

|        |   0 |   1 |
|:-------|----:|----:|
| female |  81 | 233 |
| male   | 468 | 109 |

===================================== End of report ======================================

============ Author of Dataprofile: Gordon Chen (GordonChen.GoBlue@gmail.com) ============
