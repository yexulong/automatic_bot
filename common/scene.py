# -*- coding: utf-8 -*-
import time
from abc import ABC, abstractmethod

# TODO 用状态机模式改造scene、state


class BaseState(ABC):
    """
    场景抽象类，声明子类必须实现的方法
    """
    @abstractmethod
    def handle(self, device, pic, end_pic):
        pass


class SearchState(BaseState):
    def handle(self, device, pic, end_pic, timeout=2, *args, **kwargs):
        start_time = time.time()
        while time.time() - start_time <= timeout:
            if device.find_and_click(pic, *args, **kwargs):
                return FightState()
            else:
                print('not found')
        print('not found')


class FightState(BaseState):
    def handle(self, device, pic, end_pic, *args, **kwargs):
        print('fighting')
        while not device.find_and_click(end_pic, *args, **kwargs):
            print('战斗中...')
        return SearchState()


class Scene(object):
    def __init__(self, scene):
        self.state_list = ['search', 'fight', 'finish']
        self.state = scene
        # self.transition_to(scene)

    # def get_state(self):
    #     return self._state
    #
    # def transition_to(self, scene):
    #     self._state = scene
    #     self._state.scene = self
    #
    # def handle(self, device, pic, *args, **kwargs):
    #     print(self._state)
    #     while self._state != SearchState():
    #         self.transition_to(self._state.handle(device, pic, *args, **kwargs))

    def search(self, device, pic, timeout=2, *args, **kwargs):
        # start_time = time.time()
        # while time.time()-start_time <= timeout:
        if device.find_and_click(pic, *args, **kwargs):
            self.state = 'fight'
            return 'fight'
        return None

    def fight(self, device, pic, *args, **kwargs):
        device.connect.logger.info('fighting')
        device.wait_game_img(pic, *args, **kwargs)
        device.find_and_click(pic, *args, **kwargs)
        self.state = 'finsh'
        return 'finsh'

    def finish(self, device, pos=None, pos_end=None):
        device.connect.logger.info('finish')
        x, y, x1, y1 = device.shape()
        pos = pos or (int(x / 2), int(y / 2))
        pos_end = pos_end or (int((x + x1) / 2), int((y + y1) / 2))
        device.click_bg(pos, pos_end)
        self.state = 'search'
        return 'search'


if __name__ == '__main__':
    gushi = Scene(SearchState())
    gushi.handle()
    # context1.transition_to(FightState())
    # context1.handle()
