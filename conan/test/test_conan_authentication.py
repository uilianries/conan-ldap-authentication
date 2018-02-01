#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import subprocess
import os
import signal
import time
from conans.client.conan_api import ConanAPIV1
import conans.errors
from conan.test.configuration_file import ConfigurationFile
"""Validate LDAP authentication by Conan Server
"""

class TestConanAuthentication(unittest.TestCase):
    conan_server_name = 'conan_server'
    pid = 0
    conan_api = None
    conan_server_conf_data = """
[server]
jwt_secret: MnpuzsExftskYGOMgaTYDKfw
jwt_expire_minutes: 120

ssl_enabled: False
port: 9300
public_port:
host_name: localhost

store_adapter: disk
authorize_timeout: 1800

disk_storage_path: ~/.conan_server/data
disk_authorize_timeout: 1800

updown_secret: NyiSWNWnwumTVpGpoANuyyhR

custom_authenticator: ldap_authentication

[write_permissions]

[read_permissions]
*/*@*/*: *

# Authentication type: [raw, ldap]
[auth]
type: users

[users]
"""

    @classmethod
    def setUpClass(TestConanAuthentication):
        conan_server_conf_path = os.path.join(os.path.expanduser('~'), '.conan_server', 'server.conf')
        if not os.path.exists(conan_server_conf_path):
            with open(conan_server_conf_path, 'w') as file:
                file.write(TestConanAuthentication.conan_server_conf_data)
        TestConanAuthentication.pid = subprocess.Popen(TestConanAuthentication.conan_server_name, stdout=subprocess.PIPE).pid
        time.sleep(3)
        TestConanAuthentication.conan_api, _, _ = ConanAPIV1.factory()
        TestConanAuthentication.conan_api.remote_add(remote="local", url="http://0.0.0.0:9300/")

    @classmethod
    def tearDownClass(TestConanAuthentication):
        os.kill(TestConanAuthentication.pid, signal.SIGTERM)
        TestConanAuthentication.conan_api.remote_remove(remote="local")

    def test_valid_ldap_login(self):
        TestConanAuthentication.conan_api.user(name="read-only-admin", password="password", remote="local")

    def test_invalid_ldap_login(self):
        try:
            TestConanAuthentication.conan_api.user(name="read-only-admin", password="foobar", remote="local")
            self.fail()
        except conans.errors.AuthenticationException as exception:
            self.assertEqual(str(exception), 'Wrong user or password. [Remote: local]')
