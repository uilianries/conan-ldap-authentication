#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Virtual LDAP configuration
"""
from tempfile import NamedTemporaryFile
from os import environ, path


class ConfigurationFile(object):
    test_valid_config = '''
    [ldap]
    # LDAP server address
    host: ldap://ldap.forumsys.com
    # Distinguished name (DN) of the entry
    distinguished_name: cn=$username,dc=example,dc=com
    '''

    test_wrong_config = '''
    [ldap]
    # LDAP server address
    host: ldap://ldap.forumsys
    # Distinguished name (DN) of the entry
    distinguished_name: cn=$username,dc=example,dc=com
    '''

    test_invalid_config = '''
    [server]
    # LDAP server address
    host: ldap://ldap.forumsys.com
    # Distinguished name (DN) of the entry
    distinguished_name: cn=$username,dc=example,dc=com
    '''

    @staticmethod
    def create_config_file(file_content):
        temp_file = NamedTemporaryFile(prefix="ldap-authentication-", delete=False)
        with open(temp_file.name, 'w') as file:
            file.write(file_content)
        environ["CONAN_LDAP_AUTHENTICATION_CONFIG_FILE"] = temp_file.name

    @staticmethod
    def create_valid_config():
        ConfigurationFile.create_config_file(ConfigurationFile.test_valid_config)

    @staticmethod
    def create_wrong_config():
        ConfigurationFile.create_config_file(ConfigurationFile.test_wrong_config)

    @staticmethod
    def create_invalid_config():
        ConfigurationFile.create_config_file(ConfigurationFile.test_wrong_config)
