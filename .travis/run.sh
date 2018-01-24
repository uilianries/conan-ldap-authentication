#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi
    pyenv activate conan
fi

conan user
# Validate distribution
python setup.py sdist
# Execute unit tests
mkdir -p ~/.conan_server/plugins/authenticator/
nosetests -v --with-coverage --cover-package=conan .
