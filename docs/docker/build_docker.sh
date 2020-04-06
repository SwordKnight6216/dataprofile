#!/bin/bash

html=../build/html
if [ -d "$html" ]; then
    docker build ../ -t dataprofile_web
else
    echo "please make html files before build docker"
fi
