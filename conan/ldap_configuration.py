from configparser import ConfigParser
from os.path import isfile
from os.path import expanduser
from os.path import join
from os import getenv
"""Load configuration for LDAP server

Read conf file to LDAP authenticator bind on LDAP server
"""
__author__ = "Uilian Ries"
__license__ = "MIT"


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
    @staticmethod
    def path():
        """Retrieve configuration file path

        :return: Default file path
        """
        home = expanduser('~')
        default_path = join(home, ".conan_server", "plugins", "authenticator",
                            "ldap_authentication.conf")
        return getenv("CONAN_LDAP_AUTHENTICATION_CONFIG_FILE", default_path)

    @staticmethod
    def create(filename):
        """Create default config file if **NOT** present

        :param filename: File path
        """
        if not isfile(filename):
            default_config_file = '''[ldap]
            # LDAP server address
            host: ldap://ldap.org
            # LDAP server port
            port: 9300
            # Distinguished name (DN) of the entry
            distinguished_name: ou=people,dc=example,dc=com
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
    def port(self):
        return self.__config["ldap"]["port"]

    @property
    def dn(self):
        return self.__config["ldap"]["distinguished_name"]

    def dn_with_cn(self, username):
        return self.dn.replace("%username%", username)
