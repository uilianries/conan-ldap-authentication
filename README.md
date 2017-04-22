[![Build Status](https://travis-ci.org/uilianries/conan-ldap-authentication.svg?branch=master)](https://travis-ci.org/uilianries/conan-ldap-authentication) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
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

1) Add custom_authenticator: ldap_authentication in the server.conf [server] section
2) Configure you LDAP server information in the ldap_authentication.conf [ldap] section 

To obtain more information, how to use a custom authentication in Conan.io, read the [Authentication section](https://conanio.readthedocs.io/en/latest/server.html?highlight=authentication)
  
## Usage

Just call conan authentication, as before

    $ conan user -p my_ldap_password my_ldap_username
    
Conan will use your username and password to authenticate to registered LDAP server.

## License
[MIT](LICENSE.md)


