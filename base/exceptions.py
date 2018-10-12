# -*- coding:utf-8 -*-

####################################################################################
#
# Copyright © 2017 TU. All Rights Reserved.
#
####################################################################################

"""

@File: exceptions.py

@Description: 异常

@Author: leiyunfei(leiyunfei@tuyoogame.com)

@Depart: 棋牌中心-斗地主项目组

@Create: 2017-06-05 16:16:56

"""


class FSTException(Exception):

    EXCEPT_CONFIG_ERROR = -1
    EXCEPT_KEY_ERROR = -2

    def __init__(self, error_code, message):
        super(LTException, self).__init__(error_code, message)

    @property
    def error_code(self):
        return self.args[0]

    @property
    def what(self):
        return self.args[1]

    def __str__(self):
        return '%s: %s' % (self.error_code, self.what)

    def __unicode__(self):
        return u'%s: %s' % (self.error_code, self.what)


class FSTConfigException(FSTException):

    def __init__(self, config, message):
        super(FSTConfigException, self).__init__(self.EXCEPT_CONFIG_ERROR, message)
        self.config = config

    def __str__(self):
        return '%s:%s:%s' % (self.error_code, self.what, self.config)

    def __unicode__(self):
        return u'%s:%s:%s' % (self.error_code, self.what, self.config)

