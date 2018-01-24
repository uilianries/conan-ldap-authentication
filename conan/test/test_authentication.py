import unittest
from tempfile import NamedTemporaryFile
from os import environ
from conan import ldap_authentication
"""Validation for LDAP authenticator
"""


class TestAuthentication(unittest.TestCase):
    __test_config = '''
[ldap]
# LDAP server address
host: ldap://ldap.forumsys.com
# Distinguished name (DN) of the entry
distinguished_name: cn=$username,dc=example,dc=com
'''

    __test_wrong_config = '''
[ldap]
# LDAP server address
host: ldap://ldap.forumsys
# Distinguished name (DN) of the entry
distinguished_name: cn=$username,dc=example,dc=com
'''

    __test_invalid_config = '''
[server]
# LDAP server address
host: ldap://ldap.forumsys.com
# Distinguished name (DN) of the entry
distinguished_name: cn=$username,dc=example,dc=com
'''

    def setUp(self):
        self.__create_config_file(TestAuthentication.__test_config)

    def test_valid_login(self):
        authenticator = ldap_authentication.get_class()
        self.assertTrue(authenticator.valid_user(username="read-only-admin", password="password"))

    def test_invalid_username(self):
        authenticator = ldap_authentication.get_class()
        self.assertFalse(authenticator.valid_user(username="write-only-admin", password="password"))

    def test_invalid_password(self):
        authenticator = ldap_authentication.get_class()
        self.assertFalse(authenticator.valid_user(username="read-only-admin", password="foobar"))

    def test_invalid_server(self):
        self.__create_config_file(TestAuthentication.__test_wrong_config)
        authenticator = ldap_authentication.get_class()
        self.assertFalse(authenticator.valid_user(username="read-only-admin", password="foobar"))

    def test_invalid_config(self):
        self.__create_config_file(TestAuthentication.__test_invalid_config)
        authenticator = ldap_authentication.get_class()
        self.assertFalse(authenticator.valid_user(username="read-only-admin", password="foobar"))

    def test_empty_password(self):
        authenticator = ldap_authentication.get_class()
        self.assertFalse(authenticator.valid_user(username="read-only-admin", password=None))

    def test_empty_username(self):
        authenticator = ldap_authentication.get_class()
        self.assertFalse(authenticator.valid_user(username=None, password="password"))

    def __create_config_file(self, file_content):
        self.__temp_file = NamedTemporaryFile(prefix="ldap-authentication-", delete=False)
        with open(self.__temp_file.name, 'w') as file:
            file.write(file_content)
        environ["CONAN_LDAP_AUTHENTICATION_CONFIG_FILE"] = self.__temp_file.name
