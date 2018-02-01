[![Build Status](https://travis-ci.org/uilianries/conan-ldap-authentication.svg?branch=master)](https://travis-ci.org/uilianries/conan-ldap-authentication)
[![codecov](https://codecov.io/gh/uilianries/conan-ldap-authentication/branch/master/graph/badge.svg)](https://codecov.io/gh/uilianries/conan-ldap-authentication)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pypi Download](https://img.shields.io/badge/download-pypi-blue.svg)](https://pypi.python.org/pypi/conan-ldap-authentication)
# Conan LDAP Authentication

A LDAP authentication plugin for [Conan.io](https://conan.io)

## Features
* Authenticate to Conan server, through your LDAP server
* Customize host address, port and DN

## Installation

    $ pip install conan_ldap_authentication

Or you can [clone this repository](http://github.com/uilianries/conan-ldap-authentication) and store its location in PYTHONPATH.

## Configuration

To configure the LDAP authentication in Conan, you need follow two steps:

1) Add custom authenticator in  *~/.conan_server/server.conf*
```
[server]
jwt_secret: ****
jwt_expire_minutes: 120

ssl_enabled: False
port: 9300
public_port:
host_name: localhost

# Check docs.conan.io to implement a different authenticator plugin for conan_server
# if custom_authenticator is not specified, [users] section will be used to authenticate
# the users.
#
custom_authenticator: ldap_authentication

[write_permissions]
# "opencv/2.3.4@lasote/testing": default_user,default_user2

[read_permissions]
# opencv/1.2.3@lasote/testing: default_user default_user2
# By default all users can read all blocks
*/*@*/*: *

[users]
demo: demo
```
2) Configure you LDAP server information in *~/.conan_server/ldap_authentication.conf*
```
[ldap]
# LDAP server address
host: ldap://ldap.company.org
# Distinguished name (DN) of the entry
distinguished_name: cn=$username,ou=Users,dc=company,dc=org

```

You could customize *ldap_authentication.conf* path, by CONAN_LDAP_AUTHENTICATION_CONFIG_FILE
```shell
$ export CONAN_LDAP_AUTHENTICATION_CONFIG_FILE=/etc/conan/cofig/ldap_authentication.conf
```

To obtain more information, how to use a custom authentication in Conan.io, read the [Authentication section](https://conanio.readthedocs.io/en/latest/server.html?highlight=authentication)

## Usage

Just call conan authentication, as before

    $ conan user -p my_ldap_password my_ldap_username

Conan will use your username and password to authenticate to registered LDAP server.

## Tests and Development

To run all unit tests:

    $ nosetests -v --with-coverage --cover-package=conan .

## Dependencies

The package **pyLDAP** needs a bunch of packages installed, without these packages, the installation will fail.

* python-dev
* libldap2-dev
* libsasl2-dev
* libssl-dev

## License
[MIT](LICENSE.md)
