# -*- coding: utf-8 -*-
import time
from abc import ABC, abstractmethod


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
        while time.time()-start_time <= timeout:
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
        print('fighting')
        device.wait_game_img(pic, *args, **kwargs)
        return device.find_and_click(pic, *args, **kwargs)

    def finish(self, device):
        print('finish')
        x, y, x1, y1 = device.shape()
        device.click_bg((x/2, y/2), ((x+x1)/2, (y+y1)/2))


if __name__ == '__main__':
    gushi = Scene(SearchState())
    gushi.handle()
    # context1.transition_to(FightState())
    # context1.handle()
