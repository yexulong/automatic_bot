# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class BaseScene(ABC):
    """
    场景抽象类，声明子类必须实现的方法
    """
    @abstractmethod
    def search(self):
        pass

    @abstractmethod
    def fight(self):
        pass

    @abstractmethod
    def success(self):
        pass

    @abstractmethod
    def fail(self):
        pass

    @abstractmethod
    def exit(self):
        pass


class SearchScene(BaseScene):
    def search(self, ):
        pass

    def fight(self):
        pass

    def success(self):
        pass

    def fail(self):
        pass

    def exit(self):
        pass


class Context(object):
    _scene = None

    def __init__(self, scene):
        self.transition_to(scene)

    def get_scene(self):
        return self._scene

    def transition_to(self, scene):
        self._scene = scene
        self._scene.context = self

    def search(self):
        self.transition_to(self._scene.search())

    def fight(self):
        self.transition_to(self._scene.fight())

    def success(self):
        self.transition_to(self._scene.success())

    def fail(self):
        self.transition_to(self._scene.fail())

    def exit(self):
        self.transition_to(self._scene.exit())
