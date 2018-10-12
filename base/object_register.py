# -*- coding:utf-8 -*-

###############################################################################
#
# Copyright © 2018 Fast. All Rights Reserved.
#
###############################################################################

"""

@File: reflection.py

@Description:

@Author: leiyunfei(yun63@126.com)

@Depart:

@Create: 2018-07-05 19:06:48

"""


class ClassRegister(object):
    """
    类注册器
    """

    __TYPE_ID_CLASS_MAP = {}

    @classmethod
    def find_class(cls, type_id):
        """
        根据类型，返回对应的注册对象
        """
        return cls.__TYPE_ID_CLASS_MAP.get(type_id)

    @classmethod
    def register_class(cls, type_id, clz):
        """
        注册类对象，并与之对应的type_id映射关联起来
        注册的type_id不允许重复
        """
        clzz = cls.find_class(type_id)
        if clzz:
            raise TypeError('%s already registered % for type %s' %
                           (cls, clzz, type_id))
        cls.__TYPE_ID_CLASS_MAP[type_id] = clz

    @classmethod
    def unregister_class(cls, type_id):
        """
        取消注册类对象
        """
        if type_id in cls.__TYPE_ID_CLASS_MAP:
            del cls.__TYPE_ID_CLASS_MAP[type_id]

