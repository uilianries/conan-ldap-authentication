#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from os import environ, path, makedirs
from conan import ldap_authentication
from conan.test.configuration_file import ConfigurationFile
"""Validation for LDAP authenticator
"""

class TestAuthentication(unittest.TestCase):
    @classmethod
    def setUpClass(TestAuthentication):
        user_home = environ.get("HOME")
        name = path.join(user_home, '.conan_server', 'plugins', 'authentication')
        if not path.exists(name):
            makedirs(name=name)

    @classmethod
    def tearDownClass(TestAuthentication):
        del environ["CONAN_LDAP_AUTHENTICATION_CONFIG_FILE"]

    def setUp(self):
        ConfigurationFile.create_valid_config()

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
        ConfigurationFile.create_wrong_config()
        authenticator = ldap_authentication.get_class()
        self.assertFalse(authenticator.valid_user(username="read-only-admin", password="foobar"))

    def test_invalid_config(self):
        ConfigurationFile.create_invalid_config()
        authenticator = ldap_authentication.get_class()
        self.assertFalse(authenticator.valid_user(username="read-only-admin", password="foobar"))

    def test_empty_password(self):
        authenticator = ldap_authentication.get_class()
        self.assertFalse(authenticator.valid_user(username="read-only-admin", password=None))

    def test_empty_username(self):
        authenticator = ldap_authentication.get_class()
        self.assertFalse(authenticator.valid_user(username=None, password="password"))
