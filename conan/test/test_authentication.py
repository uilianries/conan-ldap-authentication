import unittest
from tempfile import NamedTemporaryFile
from os import environ
from os.path import isfile
from conan import ldap_authentication
"""Validation for LDAP authenticator
"""


class TestAuthentication(unittest.TestCase):
    __test_config = '''[ldap]
# LDAP server address
host: ldap://ldap.forumsys.com
# Distinguished name (DN) of the entry
distinguished_name: cn=$username,dc=example,dc=com
'''

    def setUp(self):
        self.__temp_file = NamedTemporaryFile(prefix="ldap-authentication-", delete=False)
        with open(self.__temp_file.name, 'w') as file:
            file.write(TestAuthentication.__test_config)
        environ["CONAN_LDAP_AUTHENTICATION_CONFIG_FILE"] = self.__temp_file.name

    def runTest(self):
        self.assertTrue(isfile(self.__temp_file.name))
        authenticator = ldap_authentication.get_class()
        self.assertTrue(authenticator.valid_user(username="read-only-admin", password="password"))
