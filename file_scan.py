# -*- coding: utf-8 -*-
# @Author: FrozenString
# @Date:   2020-11-01 10:06:39
# @Last Modified by:   FrozenString
# @Last Modified time: 2020-11-01 10:22:36
import functools
import os
import re
# 递归读取文件


def build_return_list(x, y):
    x = list(x)
    x.extend(list(y))

    return x


def all_file(dir_name, skip_type=r'^UISprite.+$',skip_dir=".git|.vscode|__pycache__"):
    """
    a function to get all file in a dir
    :param dir_name: the path to get all files
    :param skip_type: the file name pattern which are skipped
    :return: the all files path
    """
    list_keep = os.listdir(dir_name)

    skip_pattern = re.compile(skip_type, flags=re.IGNORECASE)
    skip_dirs=skip_dir.split("|")
    out_list = filter(lambda x: os.path.isfile(path_combin(
        dir_name, x)) and skip_pattern.match(x) is None, list_keep)
    out_list = map(lambda x: path_combin(dir_name, x), out_list)

    dir_list = filter(lambda x: os.path.isdir(path_combin(dir_name, x)) and x not in skip_dir, list_keep)
    dir_list = map(lambda x: path_combin(dir_name, x), dir_list)
    dir_list = map(lambda x: all_file(x, skip_type), dir_list)

    out_list = list(out_list)
    dir_list = list(dir_list)

    return_list = functools.reduce(build_return_list, dir_list, out_list)

    return_list = list(return_list)

    return return_list


def path_combin(*paths):
    """
    将文件按顺序组合生成路径
    """
    if len(paths) == 1:
        return paths[0]
    else:
        return os.path.join(paths[0], path_combin(*paths[1:]))


if __name__ == "__main__":
    print(path_combin("a", "fff", "ssss", "dddd"))
