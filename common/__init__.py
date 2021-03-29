# -*- coding: utf-8 -*-
import configparser
import os


def get_config(file_name, section, key):
    """获取ini配置文件"""
    config = configparser.ConfigParser()
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0], file_name)
    config.read(path)
    return config.get(section, key)


def set_config(file_name, section, key, modify_value):
    """设置ini配置文件"""
    config = configparser.ConfigParser()
    path = os.path.join(os.path.split(os.path.realpath(__file__))[0], file_name)
    config.read(path)

    config.set(section, key, modify_value)
    # 保存修改
    with open(path, "w") as fw:
        # 使用write将修改内容写到文件中，替换原来config文件中内容
        config.write(fw)


if __name__ == '__main__':
    get_config('conf.ini', 'DEFAULT', '1')