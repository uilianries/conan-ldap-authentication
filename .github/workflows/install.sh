#!/bin/bash

set -e
set -x

pip install -U -r conan_ldap/requirements.txt
pip install -U -r conan_ldap/requirements_test.txt
pip install codecov
pip install .
