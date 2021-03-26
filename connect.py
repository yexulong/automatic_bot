# -*- coding: utf-8 -*-
import ctypes
import random
import subprocess
import time

import numpy as np
import win32api
import win32con
import win32gui

from Log import MyLog, log


class Connect(object):
    def connect(self, ):
        raise NotImplementedError()


def proc_rand_pos(pos, pos_end=None):
    if pos_end is None:
        pos_rand = pos
    else:
        if pos[0] > pos_end[0]:
            pos[0], pos_end[0] = pos_end[0], pos[0]
        if pos[1] > pos_end[1]:
            pos[1], pos_end[1] = pos_end[1], pos[1]
        pos_rand = (random.randint(pos[0], pos_end[0]), random.randint(pos[1], pos_end[1]))
    return pos_rand


class WindowsConnect(Connect):
    def __init__(self, windows_name: str, hwnd: int = 0, ):
        self.windows_name = windows_name
        if hwnd == 0:
            self.hwnd = win32gui.FindWindow(0, self.windows_name)
        else:
            self.hwnd = hwnd
        self.logger = MyLog('windows').get_logger()

    def connect(self):
        if self.hwnd == 0:
            self.logger.error('连接失败！请检查~ name:{}'.format(self.windows_name))
            return None
        else:
            self.logger.info('连接成功！hwnd:{} name:{}'.format(self.hwnd, self.windows_name))
            return self.hwnd

    @log
    def activate_window(self):
        user32 = ctypes.WinDLL('user32.dll')
        user32.SwitchToThisWindow(self.hwnd, True)

    def execute_command(self, com):
        ex = subprocess.Popen(com, stdout=subprocess.PIPE, shell=True)
        self.logger.debug('执行命令: {}'.format(com))
        out, err = ex.communicate()
        status = ex.wait()
        self.logger.debug('命令结果: {}'.format(out.decode().strip()))
        self.logger.debug('状态: {}'.format(status))
        return out.decode(), err, status

    def click_bg(self, pos, pos_end=None):
        """
        后台模拟点击
        :param pos: 要点击的坐标
        :param pos_end: 若不为空，则点击的是pos~pos_end之间的随机位置
        :return: 无
        """
        pos_rand = proc_rand_pos(pos, pos_end)

        win32gui.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE,
                             0, win32api.MAKELONG(*pos_rand))
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN,
                             0, win32api.MAKELONG(*pos_rand))
        time.sleep(random.randint(20, 80) / 1000)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP,
                             0, win32api.MAKELONG(*pos_rand))

    @log
    def drag_bg(self, pos1, pos2, cost_time=None):
        """
        后台拖拽
        :param pos1: (x,y) 起点坐标
        :param pos2: (x,y) 终点坐标
        :param cost_time: 消耗时间
        """
        move_x = np.linspace(pos1[0], pos2[0], num=20, endpoint=True)
        move_y = np.linspace(pos1[1], pos2[1], num=20, endpoint=True)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, 0, win32api.MAKELONG(*pos1))

        for i in range(20):
            x = int(round(move_x[i]))
            y = int(round(move_y[i]))
            win32gui.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
            t = 0.01 * random.random()
            time.sleep(t)
            cost_time -= t * 1000

        if cost_time > 0:
            time.sleep(cost_time / 1000)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, win32api.MAKELONG(*pos2))


class SimulatorConnect(WindowsConnect, Connect, ):
    def __init__(self, windows_name: str, hwnd: int = 0, device_id='127.0.0.1:7555'):
        super().__init__(windows_name, hwnd)
        self.device_id = device_id
        self.logger = MyLog('simulator').get_logger()

    def connect(self):
        super().connect()
        self.execute_command('adb connect {}'.format(self.device_id))
        return self.hwnd

    def click_bg(self, pos, pos_end=None):
        pos_rand = proc_rand_pos(pos, pos_end)
        self.execute_command('adb shell input tap {} {}'.format(*pos_rand))

    def drag_bg(self, pos1, pos2, cost_time=None):
        if cost_time is None:
            line = np.sqrt(np.sum(np.square(np.array(pos1) - np.array(pos2))))
            cost_time = round(random.uniform(line / 2, line))
        self.execute_command('adb shell input swipe {} {} {} {} {}'.format(*pos1, *pos2, cost_time))


if __name__ == '__main__':
    test = SimulatorConnect('阴阳师 - MuMu模拟器')
    test.connect()
    test.activate_window()
    # test.drag_bg((200, 200), (500, 200), 1500)
    # test.click_bg()
    # popo = WindowsConnect('网易POPO')
    # popo.activate_window()
    # time.sleep(2)
    # popo.drag_bg((200, 500), (1000, 500), 1500)
