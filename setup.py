import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="datareport",
    version="0.1.3",
    author="Gordon Chen",
    author_email="GordonChen.GoBlue@gmail.com",
    description="This package is used to extract metadata from any given pandas DataFrame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SwordKnight6216/datareport",
    packages=setuptools.find_packages(),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU AGPLv3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)