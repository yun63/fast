# -*- coding:utf-8 -*-

###############################################################################
#
# Copyright © 2018 TU. All Rights Reserved.
#
###############################################################################

"""

@File: lib_loader.py

@Description:

@Author: leiyunfei(leiyunfei@tuyoogame.com)

@Depart: 棋牌中心

@Create: 2019-01-21 10:22:13

"""

import os

from cffi import FFI


class LibLoader(object):
    """
    动态链接库装载器，python调用c函数，不能直接调用c++接口，请将c++导出为c函数
    """
    def __init__(self):
        self._ffi = FFI()
        self.cdef()

    def cdef(self):
        """
        必须声明接口导出
        """
        raise NotImplementedError

    @classmethod
    def loadlib(cls, so_file_name, so_dir_name):
        """
        装载动态链接库，动态链接库在脚本启动后已编译生成，脚本不负责编译库
        """
        so_path = os.path.dirname(__file__) + '/' + so_dir_name+ '/'
        so_file = os.path.abspath(so_path + so_file_name)
        return LibLoader()._ffi.dlopen(so_file)

