# -*- coding: utf-8 -*-
# @Author: FrozenString
# @Date:   2020-11-01 09:06:59
# @Last Modified by:   FrozenString
# @Last Modified time: 2020-11-01 10:16:51
from input_output import IOCtrl
import os
from tools import GitCtrl

g = GitCtrl(IOCtrl(), "./")

#g.add_files(["main.py", "input_output.py", "tools.py"])
g.add_all_files()
g.commit("第二次提交")
