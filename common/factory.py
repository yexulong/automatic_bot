# -*- coding: utf-8 -*-
from common.connect import WindowsConnect, SimulatorConnect
from common.game_enum import ConnectEnum, DeviceEnum
from common.device import Device, MuMuSimulator


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


class DeviceFactory(object):
    def __init__(self):
        self.device = None

    def get_device(self, name: str, deviceType: int = DeviceEnum.WINDOWS.value):
        if deviceType == DeviceEnum.WINDOWS.value:
            self.device = Device(name)
        elif deviceType == DeviceEnum.MUMU.value:
            self.device = MuMuSimulator(name)

        return self.device


if __name__ == '__main__':
    mumu = ConnectFactory().get_connect('', 0, 2)
