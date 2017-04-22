from ldap_configuration import LDAPConfiguration
from ldap_configuration import LDAPConfigFile
import ldap
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
    return LDAPAuthenticator()


class LDAPAuthenticator(object):
    """Provide LDAP authentication by PyLDAP for Conan server.

    Settings should be present in default_ldap_authentication.py, this file is in same
    """
    def __init__(self):
        config_file = LDAPConfigFile.path()
        LDAPConfigFile.create(config_file)
        self.__conf = LDAPConfiguration(config_file)
        self.__connection = ldap.initialize("%s:%s" % (self.__conf.host, self.__conf.port), ldap.SCOPE_SUBTREE)

    def valid_user(self, username, password):
        self.__connection.simple_bind_s(username, password)
        return self.__connection.search_s(self.__conf.dn_with_cn(username))