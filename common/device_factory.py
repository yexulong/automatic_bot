# -*- coding: utf-8 -*-
from device import Device, MuMuSimulator
from game_enum import DeviceEnum


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
    mumu = DeviceFactory().get_device('MuMu模拟器', DeviceEnum.MUMU.value)