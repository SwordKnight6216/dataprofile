"""File to configure wheel build."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="dataprofile",
    version="2.1.0",
    author="Gordon Chen",
    author_email="GordonChen.GoBlue@gmail.com",
    license="GNU Affero General Public License v3.0",
    description="This package generates statistical reports for given pandas DataFrames "
                "or CSV files in standalone model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SwordKnight6216/dataprofile",
    packages=setuptools.find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU AGPLv3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={'console_scripts': ['dataprofile_single=dataprofile.cli_report:render_single_file_report',
                                      'dataprofile_all=dataprofile.batch_cli_reports:render_reports_for_all']}
)
