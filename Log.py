# -*- coding: utf-8 -*-
import functools
import logging
import os

from common import get_config


class MyLog(object):
    def __init__(self, logger_name="example"):
        # create logger
        self.logger_name = logger_name
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.DEBUG)

        # create file handler
        self.log_base_path = './log'
        self.log_path = "{}/{}.log".format(self.log_base_path, self.logger_name)
        if not os.path.exists(self.log_base_path):
            os.mkdir(self.log_base_path)
        self.fh = logging.FileHandler(self.log_path, encoding='utf8')
        fh_level = get_config('conf.ini', 'LOG', 'level')
        self.fh.setLevel(logging.getLevelName(fh_level))

        # create stream handler
        self.sh = logging.StreamHandler()
        self.sh.setLevel(logging.DEBUG)

        # create formatter
        self.fmt = "[%(asctime)s][%(levelname)s][%(name)s][%(process)d][%(filename)s][%(funcName)s][line:%(lineno)d] %(message)s"
        self.datefmt = "%Y-%m-%d %H:%M:%S"
        self.formatter = logging.Formatter(self.fmt, self.datefmt)

        # add handler and formatter to logger
        self.fh.setFormatter(self.formatter)
        self.sh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.sh)

    def get_logger(self):
        return self.logger


def log(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self.logger.debug('{} 函数运行...'.format(func.__name__))
        print(func.__class__)
        result = func(self, *args, **kwargs)
        self.logger.debug('{} 函数结束...'.format(func.__name__))
        return result

    return wrapper


if __name__ == '__main__':
    logger = MyLog(logger_name='hahaha', ).get_logger()
    logger.debug('test')
