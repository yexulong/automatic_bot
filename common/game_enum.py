# -*- coding: utf-8 -*-
from enum import Enum, unique


@unique
class ConnectEnum(Enum):
    WINDOWS_APP = 1
    MUMU = 2
    YESHEN = 3


class DeviceEnum(Enum):
    WINDOWS = 1
    MUMU = 2
    YESHEN = 3
