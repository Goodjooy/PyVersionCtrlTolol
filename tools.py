# -*- coding: utf-8 -*-
# @Author: FrozenString
# @Date:   2020-11-01 09:11:16
# @Last Modified by:   FrozenString
# @Last Modified time: 2020-11-01 17:43:06
from typing import Pattern
from file_scan import all_file
from input_output import IOCtrl
import os
import re
import functools
# git交互方法类


def cmd_info(cmd, io):
    infos = os.popen(cmd)
    info = infos.buffer.read().decode("utf8")
    io.info_out_put(info)
    io.info_out_put("\n")
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

        self.history_commit_id = []

    def _appends(self, logs):
        patten = re.compile(r'commit ([a-z0-9]+)\n', re.IGNORECASE)
        t_logs = patten.findall(logs)
        for t in t_logs:
            if t in self.history_commit_id:
                pass
            else:
                self.history_commit_id.extend(t)

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
        cmd = f"{self.gitpath} log"
        log = cmd_info(cmd, self.io)
        self._appends(log)

    def version_back(self, version_id="HEAD^"):
        """
        git控制版本回退
        """
        cmd = f'{self.gitpath} reset --hard {version_id}'
        cmd_info(cmd, self.io)

    def get_status(self):
        cmd = f"{self.gitpath} status"
        cmd_info(cmd, self.io)
        # TODO 解析分支信息，生成信息

    def get_diff(self, branch, filename):
        cmd = f"{self.gitpath} diff {branch} -- {filename}"
        cmd_info(cmd, self.io)

    def Checkout_workspace(self, filename):
        """
        将工作区的改变撤回
        """
        cmd = f"{self.gitpath} checkout -- {filename}"
        cmd_info(cmd, self.io)

    def unstage_added(self, filename, commit_id="HEAD"):
        """
        撤销暂存区的暂存的内容
        """
        cmd = f"{self.gitpath} reset {commit_id} {filename}"
        cmd_info(cmd, self.io)

    def remove(self, filename):
        cmd = f"{self.gitpath} rm {filename}"

    def link_git(self, target_git, targrt_gitsite="Github.com", commit_name="origin"):
        """
        链接远程仓库
        """
        cmd = f"{self.gitpath} remote add {commit_name} git@{targrt_gitsite}:{target_git}"
        cmd_info(cmd, self.io)

    def push_git(self, branch="master", commit_name="origin", is_first=True):
        t = ""
        if is_first:
            t = "-u"
        cmd = f"{self.gitpath} push {t} {commit_name} {branch}"
        cmd_info(cmd, self.io)

    def clone_git_ssh(self, target_git, target_gitsite="Github.com"):
        """
        使用ssh克隆仓库
        """
        cmd = f"{self.gitpath} clone git@{target_gitsite}:{target_git}"
        cmd_info(cmd, self.io)
