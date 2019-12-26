# -*- coding:utf-8 -*-

###############################################################################
#
# Copyright © 2018 TU. All Rights Reserved.
#
###############################################################################

"""

@File: iphostname_test.py

@Description:

@Author: leiyunfei(leiyunfei@tuyoogame.com)

@Depart: 棋牌中心

@Create: 2018-12-28 18:03:19

"""

import unittest
import sys
import socket
import logging
import netifaces

from iphostname import local_ipv4_addrs, local_ipv6_addrs, \
        local_hostnames, local_interface_names, \
        is_valid_ipv4, is_valid_ipv6


LOG = logging.getLogger(__name__)


class TestIPHostname(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testLocalIpv4Addr(self):
        LOG.info('local ipv4 addresses are: %s', local_ipv4_addrs())

    def testLocalIpv6Addr(self):
        LOG.info('local ipv6 addresses are: %s', local_ipv6_addrs())

    def testLocalInterfaceNames(self):
        LOG.info('local net interface names are: %s', local_interface_names())

    def testLocalHostnames(self):
        LOG.info('local host names are: %s', local_hostnames())


class TestIPValidator(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testIsValidIpv4(self):
        self.assertTrue(is_valid_ipv4('10.1.111.111'))
        self.assertFalse(is_valid_ipv4('300.1.111.111'))

    def testIsValidIpv6(self):
        self.assertTrue(is_valid_ipv6('fe80::290:9eff:fe9a:a9b7%en4'))


def main():
    unittest.main()

if __name__ == '__main__':
    sys.exit(int(main() or 0))
