# dataprofile
> This package is used to render statistical reports for CSV files. The reports can be saved as txt, markdown, or html format.

## Sample reports

[txt format](sample_reports/titanic/report_titanic.txt)  
[markdown format](sample_reports/titanic/report_titanic.md)  
[html format](sample_reports/titanic/report_titanic.html)  

## Installation

```sh
git clone https://github.com/SwordKnight6216/dataprofile.git
cd dataprofile
pip install -e .
```

## How to use
1. in python scripts
    ```python
    import dataprofile
    ```
2. from command line
   ```shell script
   python dataprofile/scripts/cli_report.py 
   ```
3. from docker
   ```shell script
   docker pull swordknight6216/dataprofile
   docker run -ti --rm -v $(pwd):/home/dp_user/data swordknight6216/dataprofile
   ```

## Documentation

[documentation](docs/build/html/index.html)

## Meta

Gordon Chen – [LinkedIn](https://www.linkedin.com/in/gordonchendatascientist/) – GordonChen.GoBlue@gmail.com

Distributed under the GNU AFFERO GENERAL PUBLIC LICENSE license. See ``LICENSE`` for more information.

[https://github.com/GordonChen/github-link](https://github.com/SwordKnight6216)