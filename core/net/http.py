# -*- coding:utf-8 -*-

###############################################################################
#
# Copyright © 2018 TU. All Rights Reserved.
#
###############################################################################

"""

@File: http.py

@Description:

@Author: leiyunfei(leiyunfei@tuyoogame.com)

@Depart: 棋牌中心

@Create: 2018-12-28 12:54:43

"""

import json
import requests
import logging


LOG = logging.getLogger(__name__)


def __send_request(url, method='get', query_params={}, timeout=3, post_data={}, headers={}):
    """
    Returns: class:'Response <Response>' object
    """
    if hasattr(requests, method):
        action_func = getattr(requests, method)
        r = action_func(url, params=query_params, json=post_data, headers=headers, timeout=timeout)
        return r
    raise Exception('method %s not supported' % method)


def http_json_request(url, method='get', query_params={}, timeout=3,
        post_data={}, headers={'content-type': 'application/json'}):
    try:
        r = __send_request(url=url, method=method, query_params=query_params, timeout=timeout,
                post_data=post_data, headers=headers)
        return r.json()
    except:
        LOG.error('request (json) % failed.', url, exc_info=True)


def http_status_request(url, method='get', query_params={}, timeout=3,
        post_data={}, headers={}):
    try:
        r = __send_request(url=url, method=method, query_params=query_params, timeout=timeout,
                post_data=post_data, headers=headers)
        return r.status_code
    except:
        LOG.error('request (status) % failed.', url, exc_info=True)

