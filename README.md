# dataprofile
> This package is used to render statistical reports for CSV files. The reports can be saved as txt, markdown, or html format.

## Sample reports

[txt format](sample_reports/titanic/report_titanic.txt)  
[markdown format](sample_reports/titanic/report_titanic.md)  
[html format](sample_reports/titanic/report_titanic.html)  

## Installation

### For Users
```sh
git clone https://github.com/SwordKnight6216/dataprofile.git
cd dataprofile
pip install .
```

### For Developers
```sh
git clone https://github.com/SwordKnight6216/dataprofile.git
cd dataprofile
pip install -e ".[dev]"  # Installs package in editable mode with development dependencies
```

## How to use
1. In Python scripts
    ```python
    import dataprofile
    ```

2. From command line
    ```shell script
    dataprofile_single
    dataprofile_all
    ```

3. From Docker
    ```shell script
    docker run -ti --rm -v $(pwd):/home/dp_user/data swordknight6216/dataprofile
    ```

## Development

### Running Tests
```sh
pytest
```

### Type Checking
```sh
mypy
```

### Linting
```sh
flake8
```

### Generating Requirements Files (optional)
```sh
# Install pip-tools
pip install pip-tools

# Generate requirements files
pip-compile --output-file=requirements.txt pyproject.toml
pip-compile --extra=dev --output-file=requirements-dev.txt pyproject.toml
```

## Documentation

[documentation](docs/build/html/index.html)

## Meta

Gordon Chen – [LinkedIn](https://www.linkedin.com/in/gordonchendatascientist/) – GordonChen.GoBlue@gmail.com

Distributed under the GNU AFFERO GENERAL PUBLIC LICENSE license. See `LICENSE` for more information.

[https://github.com/GordonChen/github-link](https://github.com/SwordKnight6216)
