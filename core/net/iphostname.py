# -*- coding:utf-8 -*-

###############################################################################
#
# Copyright © 2018 TU. All Rights Reserved.
#
###############################################################################

"""

@File: iphostname.py

@Description:

@Author: leiyunfei(leiyunfei@tuyoogame.com)

@Depart: 棋牌中心

@Create: 2018-12-28 17:56:22

"""

import socket
import netifaces


def __local_ip_addrs(family):
    """
    Get the ip addresses on this port
    Args:
    @family: socket.AF_INET or socket.AF_INET6
    """
    ipaddr_list = []
    iface_list = netifaces.interfaces()

    for iface in iface_list:
        network_lines = netifaces.ifaddresses(iface).get(family, [])
        for network in network_lines:
            ipaddr_list.append(network['addr'])
    return ipaddr_list


def local_ipv4_addrs():
    """
    Get the ipv4 addresses of all net inetfaces on this port
    """
    return __local_ip_addrs(family=netifaces.AF_INET)


def local_ipv6_addrs():
    """
    Get the ipv6 addresses of all net inetfaces on this port
    """
    return __local_ip_addrs(family=netifaces.AF_INET6)


def local_hostnames():
    """
    Get the local host names
    Return: a list of host name str
    """
    return [socket.gethostname(), socket.getfqdn()]


def local_interface_names():
    return netifaces.interfaces()


def is_valid_ipv4(ipv4_str):
    try:
        socket.inet_pton(socket.AF_INET, ipv4_str)
        return True
    except:
        return False


def is_valid_ipv6(ipv6_str):
    try:
        socket.inet_pton(socket.AF_INET6, ipv6_str)
        return True
    except:
        return False

