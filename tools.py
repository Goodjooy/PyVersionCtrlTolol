# -*- coding: utf-8 -*-
# @Author: FrozenString
# @Date:   2020-11-01 09:11:16
# @Last Modified by:   FrozenString
# @Last Modified time: 2020-11-01 10:41:09
from typing import Pattern
from file_scan import all_file
from input_output import IOCtrl
import os
import re
import functools
# git交互方法类


def cmd_info(cmd, io):
    infos = os.popen(cmd)
    info=infos.buffer.read().decode("utf8")
    io.info_out_put(info)
    # for info in infos.readlines():
    #    io.info_out_put(info)
    return info


class GitCtrl(object):
    def __init__(self, ioCtrl, path, gitpath="git", reinit=False):
        """
        初始化git仓库
        """
        self.gitpath = f"\"{gitpath}\""
        self.path = ""
        if os.path.isabs(path):
            self.path = path
        else:
            self.path = os.path.abspath(path)

        if isinstance(ioCtrl, IOCtrl):
            self.io = ioCtrl
        else:
            self.io = IOCtrl()

        # 检查目标目录下是否有.git文件夹
        if os.path.exists(os.path.join(path, ".git")) and not reinit:
            pass
        else:
            # 新建仓库
            cmd = f"{self.gitpath} init \"{path}\""
            cmd_info(cmd, self.io)

        self.history_commit_id=[]
    
    def _appends(self,logs):
        patten=re.compile(r'commit ([a-z0-9]+)\n',re.IGNORECASE)
        t_logs=patten.findall(logs)
        for t in t_logs:
            if t in self.history_commit_id:
                pass
            else:
                self.history_commit_id.extend(t);

    def add_files(self, filenames):
        target_files = functools.reduce(
            lambda x, y: f"{x} \"{os.path.abspath(y)}\"", filenames, "")
        cmd = f"{self.gitpath} add {target_files}"
        cmd_info(cmd, self.io)

    def add_all_files(self, except_file_patten=r'^$', except_dir=r".git|.vscode|__pycache__"):
        target_files = all_file(self.path, except_file_patten, except_dir)
        self.add_files(target_files)

    def commit(self, info):
        cmd = f"{self.gitpath} commit -m {info}"
        cmd_info(cmd, self.io)
        
    def show_commit_history(self):
        cmd=f"{self.gitpath} log"
        log=cmd_info(cmd,self.io)
        self._appends(log)
    def Version_back(self, back_times):
        """
        git控制版本回退
        """
        
