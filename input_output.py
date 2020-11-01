# -*- coding: utf-8 -*-
# @Author: FrozenString
# @Date:   2020-11-01 09:26:12
# @Last Modified by:   FrozenString
# @Last Modified time: 2020-11-01 09:29:17


class IOCtrl(object):
    
    def info_out_put(info):
        """
        信息输出方法
        """
        print(info)
    
    def show_with_str_enter(self, info):
        """
        显示信息，并获取str类型的输入数据
        """
        return input(info)