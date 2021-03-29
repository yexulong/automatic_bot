# -*- coding: utf-8 -*-
from common.connect import WindowsConnect, SimulatorConnect
from common.game_enum import ConnectEnum


# from common.device import Device, MuMuSimulator


class ConnectFactory(object):
    def __init__(self):
        self.connect = None

    def get_connect(self, name: str = None, hwnd: int = 0, connectType: int = ConnectEnum.WINDOWS_APP.value):
        if connectType == ConnectEnum.WINDOWS_APP.value:
            # self.connect = WindowsAPPConnect(name, hwnd)
            self.connect = WindowsConnect(name, hwnd)
        elif connectType == ConnectEnum.MUMU.value:
            # self.connect = MuMuConnect(name, hwnd)
            self.connect = SimulatorConnect(name, hwnd)
        # elif connectType == ConnectEnum.YESHEN.value:
        #     self.connect = YeShenConnect(name, hwnd)
        self.connect.connect()
        return self.connect


if __name__ == '__main__':
    mumu = ConnectFactory().get_connect('', 0, 2)
