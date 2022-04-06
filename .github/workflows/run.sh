#!/bin/bash

set -e
set -x

conan user
# Validate distribution
python setup.py sdist
# Execute unit tests
nosetests -v --with-coverage --cover-package=conan_ldap conan_ldap.test
