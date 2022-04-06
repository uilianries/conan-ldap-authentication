#!/bin/bash

set -e
set -x

pip install -U -r conan/requirements.txt
pip install -U -r conan/requirements_test.txt
pip install codecov
pip install .
