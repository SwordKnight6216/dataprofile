from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="dataprofile",
    version="2.1.0",
    author="Gordon Chen",
    author_email="GordonChen.GoBlue@gmail.com",
    description="This package generates statistical reports for given pandas DataFrames or CSV files in standalone model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SwordKnight6216/dataprofile",
    packages=find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU AGPLv3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension('dataprofile._var_statistics',
                            ['dataprofile/_var_statistics.pyx'])]
)
