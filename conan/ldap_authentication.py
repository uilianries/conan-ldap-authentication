# -*- coding: utf-8 -*-
import ldap
from configparser import ConfigParser
from os.path import isfile
from os.path import expanduser
from os.path import join
from os import getenv
from logging import warning
"""LDAP Authenticator for Conan Project.

This module offers LDAP authentication with Conan Server.

Example:
    The user can normally apply his username and password, as before

        $ conan user -p my_password my_username

Conan will call this authenticator to provide a custom validation by LDAP.

Settings:
    host: LDAP server address.
        e.g ldap://host:port

    distinguished_name: A DN is a sequence of relative distinguished names
                       (RDN) connected by commas.
        e.g. uid=my_username,ou=people,dc=example,dc=com

Dependencies:
    This project uses **PyLDAP** to connect LDAP server


   https://github.com/uilianries/conan-ldap-authenticator
"""
__author__ = "Uilian Ries"
__license__ = "MIT"


def get_class():
    """Entry point for Conan Server call this custom authenticator

    :return: The LDAP authenticator instance
    """
    LDAPConfigFile()
    return LDAPAuthenticator()


class LDAPConfigurationException(Exception):
    """Configuration Exception

    Prefix message for configuration
    """
    def __init__(self, value):
        self.value = "ERROR: Could not load configuration: %s " % value

    def __str__(self):
        return repr(self.value)


class LDAPConfigFile(object):
    """Create and retrieve configuration file

    """
    def __init__(self):
        LDAPConfigFile.__create(self.path())

    @staticmethod
    def path():
        """Retrieve configuration file path

        :return: Default file path
        """
        home = expanduser('~')
        default_path = join(home, ".conan_server", "ldap_authentication.conf")
        return getenv("CONAN_LDAP_AUTHENTICATION_CONFIG_FILE", default_path)

    @staticmethod
    def __create(filename):
        """Create default config file if **NOT** present

        :param filename: File path
        """
        if not isfile(filename):
            default_config_file = '''
[ldap]
# LDAP server address
host: ldap://ldap.forumsys.com
# Distinguished name (DN) of the entry
distinguished_name: cn=$username,dc=example,dc=com
'''
            with open(filename, "w") as text_file:
                text_file.write(default_config_file)


class LDAPConfiguration(object):
    """Configuration entity for LDAP authenticator

    Load config file and each property
    """
    def __init__(self, filename):
        LDAPConfiguration.__check_filename(filename)
        self.__config = ConfigParser()
        self.__config.read(filename)

    @staticmethod
    def __check_filename(filename):
        if not isfile(filename):
            raise LDAPConfigurationException("File name doest not exist")

    @property
    def host(self):
        return self.__config["ldap"]["host"]

    @property
    def dn(self):
        return self.__config["ldap"]["distinguished_name"]

    def dn_with_cn(self, username):
        return self.dn.replace("$username", username)


class LDAPAuthenticator(object):
    """Provide LDAP authentication by PyLDAP for Conan server.

    Settings should be present in default_ldap_authentication.py, this file is in same
    """
    def valid_user(self, username, password):
        result = False
        try:
            if not username:
                raise Exception('Empty username provided.')
            if not password:
                raise Exception('Empty password provided.')
            config_file = LDAPConfigFile().path()
            conf = LDAPConfiguration(config_file)
            connection = ldap.initialize(conf.host)
            connection.simple_bind_s(conf.dn_with_cn(username), password)
            result = True
        except Exception as error:
            warning(str(error))
        return result
