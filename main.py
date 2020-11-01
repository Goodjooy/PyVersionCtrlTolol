# -*- coding: utf-8 -*-
# @Author: FrozenString
# @Date:   2020-11-01 09:06:59
# @Last Modified by:   FrozenString
# @Last Modified time: 2020-11-01 09:09:11
import os
output =os.popen("git add main.py")

print(output.readlines())

output=os.popen("git commit -m \"全新的小工具\"")
print(output.readlines())