# -*- coding:utf-8 -*-

###############################################################################
#
# Copyright © 2018 TU. All Rights Reserved.
#
###############################################################################

"""

@File: ssh_test.py

@Description:

@Author: leiyunfei(leiyunfei@tuyoogame.com)

@Depart: 棋牌中心

@Create: 2018-12-28 18:08:06

"""

import sys
import unittest
from functools import partial

from ssh import remote_ssh_login, PasswordAuthException, remote_ssh_exec_cmd, SSHConnectException


class SSHTest(unittest.TestCase):

    def setUp(self):
        self.username = 'tuyoo'

        self.password_ok = '123456'
        self.password_nook = '1234qwer'

        self.hostname_ok = '172.16.0.28'
        self.hostname_nook = '10.1.123.18'

        self.timeout = 20


    def tearDown(self):
        pass

    def test_remote_ssh_login(self):
        self.assertTrue(
            remote_ssh_login(
                hostname=self.hostname_ok,
                username=self.username,
                timeout=self.timeout,
                password=self.password_ok
            )
        )

        result = remote_ssh_login(hostname=self.hostname_ok,
                password=self.password_nook,
                username=self.username,
                timeout=self.timeout
                )
        print result
        self.assertFalse(result)
        '''
        self.assertFalse(
            remote_ssh_login(
                hostname=self.hostname_ok,
                password=self.password_nook,
                username=self.username,
                timeout=self.timeout
            )
        )
        '''

        with self.assertRaises(SSHConnectException):
            remote_ssh_login(
                hostname=self.hostname_nook,
                password=self.password_ok,
                username=self.username,
                timeout=self.timeout
            )


    def test_remote_ssh_exec_cmd(self):
        cmdout, cmderr = remote_ssh_exec_cmd(
            command='uname -r',
            hostname=self.hostname_ok,
            username=self.username,
            timeout=self.timeout,
            password=self.password_ok,
        )
        self.assertEqual('3.10.0-957.1.3.el7.x86_64\n', cmdout)


def main():
    unittest.main()

if __name__ == '__main__':
    sys.exit(int(main() or 0))
