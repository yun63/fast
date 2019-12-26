# -*- coding:utf-8 -*-

###############################################################################
#
# Copyright © 2018 TU. All Rights Reserved.
#
###############################################################################

"""

@File: ssh.py

@Description:

@Author: leiyunfei(leiyunfei@tuyoogame.com)

@Depart: 棋牌中心

@Create: 2018-12-28 18:07:38

"""

import logging
import socket
import paramiko


LOG = logging.getLogger(__name__)


class SSHConnectException(Exception):
    pass


class PasswordAuthException(Exception):
    pass


def __new_sshclient():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    return client


def __new_logined_sshclient(hostname, username, password, port=22, timeout=2):
    try:
        client = __new_sshclient()
        client.connect(hostname=hostname, username=username, password=password, port=port, timeout=timeout)
        return client
    except paramiko.AuthenticationException:
        LOG.error('incorrect hostname or password', exc_info=True)
        raise PasswordAuthException()
    except (paramiko.BadHostKeyException, paramiko.SSHException) as othe:
        LOG.error('raise bad-host-key or ssh exception', exc_info=True)
        raise othe
    except (socket.error, socket.timeout) as socke:
        LOG.error('connecting host %s (%d-seconds timeout) failed',
                  hostname, timeout, exc_info=True)
        raise socke


def remote_ssh_login(hostname, username, password, port=22, timeout=2):
    """
    Check if can remote ssh login host with given username and password
    Parameters:
        - hostname (str): the hostname to connect
        - username (str): the username to login
        - password (str): the plain password of given `username`
        - port (int): remote ssh login port, defaults to 22
        - timeout (int): socket connect timeout, in seconds, defaults to 2

    Raises:
        - paramiko.BadHostKeyException:  if the server’s host key could not be verified
        - paramiko.SSHException: if there was any other error connecting
                                 or establishing an SSH session
        - socket.error: if a socket error occurred while connecting
        - socket.timeout: if socket connects with timeout
    Returns: `True` if given parameters all correct;
             if hostname is available and <username, password> incorrect, return `False`;
             else raise exception
    """
    try:
        with __new_logined_sshclient(hostname=hostname, username=username, password=password, port=port, timeout=timeout) as client:
            return True
    except PasswordAuthException:
        return False
    except Exception:
        raise SSHConnectException()


def remote_ssh_exec_cmd(command, hostname, username, password, port=22, timeout=3):
    """
    Execute given `command` on remote `hostname`
    Parameters:
        - hostname (str): the hostname to connect
        - username (str): the username to login
        - password (str): the plain password of given `username`
        - command (str): the command to execute
        - port (int): remote ssh login port, defaults to 22
        - timeout (int): socket connect timeout, in seconds, defaults to 3

    Raises:
        - `SSHConnectException`: if raise paramiko.[BadHostKeyException, SSHException]
          or socket.[error, timeout]
        - `PasswordAuthException`: if given username or password incorrect
    Returns: a tuple of (stdout-string, stderr-string)
    """

    try:
        with __new_logined_sshclient(hostname=hostname, username=username,
                                     password=password, port=port,
                                     timeout=timeout) as client:
            _, out_fp, err_fp = client.exec_command(command=command, timeout=timeout)
            return out_fp.read(), err_fp.read()
    except PasswordAuthException as pae:
        raise pae
    except Exception as e:
        raise SSHConnectException()
