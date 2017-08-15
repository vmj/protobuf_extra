#!/usr/bin/env bash

pip install protobuf==$1
python setup.py install
python -m unittest discover -v -p "unittests.py"
