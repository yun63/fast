# -*- coding:utf-8 -*-

###############################################################################
#
# Copyright © 2018 TU. All Rights Reserved.
#
###############################################################################

"""

@File: configurable.py

@Description: 可配置对象

@Author: leiyunfei(leiyunfei@tuyoogame.com)

@Depart: 棋牌中心

@Create: 2018-07-05 19:24:23

"""

from fast.base.object_register import ClassRegister
from fast.base.exceptions import FSTConfigException


class Configurable(object):

    TYPE_ID = 'unknown_type_id'

    def __init__(self):
        pass

    def parse_from_config(self, d):
        raise NotImplementedError


class ConfigureRegister(ClassRegister):

    @classmethod
    def parse_from_config(cls, config):
        type_id = config.get('type_id')
        clz = cls.find_class(type_id)
        if not clz:
            raise FSTConfigException(d, '% unknown type_id %s' % (cls, type_id))
        try:
            confable = clz()
            confable.parse_from_config(config)
        except Exception as e:
            print(e)
            raise e
        return confable

    @classmethod
    def parse_list(cls, config_list):
        ret = []
        for d in config_list:
            ret.append(cls.parse_from_config(d))
        return ret

