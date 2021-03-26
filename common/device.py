# -*- coding: utf-8 -*-
import traceback
import cv2
import win32ui

from common.connect import *
from common.factory import ConnectFactory
from common.game_enum import ConnectEnum


class Device(object):
    def __init__(self, name, connectType=1):
        """
        初始化设备，获取设备的分辨率等信息
        :param name:
        :param connectType:
        """
        self.name = name
        self.connect = ConnectFactory().get_connect(self.name, connectType=connectType)
        l1, t1, r1, b1 = win32gui.GetWindowRect(self.connect.hwnd)
        l2, t2, r2, b2 = win32gui.GetClientRect(self.connect.hwnd)
        self._offset_h = 0
        self._offset_w = 0
        self._client_h = b2 - t2
        self._client_w = r2 - l2
        self._border_l = ((r1 - l1) - (r2 - l2)) // 2
        self._border_t = ((b1 - t1) - (b2 - t2)) - self._border_l

    def init_mem(self):
        self.hwindc = win32gui.GetWindowDC(self.connect.hwnd)
        self.srcdc = win32ui.CreateDCFromHandle(self.hwindc)
        self.memdc = self.srcdc.CreateCompatibleDC()
        self.bmp = win32ui.CreateBitmap()
        self.bmp.CreateCompatibleBitmap(
            self.srcdc, self._client_w, self._client_h)
        self.memdc.SelectObject(self.bmp)

    def click_bg(self, pos, pos_end=None):
        return self.connect.click_bg(pos, pos_end)

    def drag_bg(self, pos1, pos2, cost_time):
        return self.connect.drag_bg(pos1, pos2, cost_time)

    def dump(self):
        """
        打印自身成员变量值
        :return: 成员变量: 值
        """
        for i in self.__dict__:
            print(i, ': ', getattr(self, i))

    def window_full_shot(self, file_name=None, gray=0):
        """
        窗口截图
        :param file_name: 截图文件的保存名称
        :param gray: 是否返回灰度图像，0：返回BGR彩色图像，其他：返回灰度黑白图像
        :return: file_name为空则返回RGB数据
        """
        try:
            if not hasattr(self, 'memdc'):
                self.init_mem()
            self.memdc.BitBlt((self._offset_w, self._offset_h),
                              (self._client_w - self._offset_w, self._client_h - self._offset_h), self.srcdc,
                              (self._border_l, self._border_t), win32con.SRCCOPY)

            if file_name is not None:
                self.bmp.SaveBitmapFile(self.memdc, file_name)
                return
            else:
                signedIntsArray = self.bmp.GetBitmapBits(True)
                img = np.frombuffer(signedIntsArray, dtype='uint8')
                img.shape = (self._client_h, self._client_w, 4)
                if gray == 0:
                    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                else:
                    return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        except Exception:
            self.init_mem()
            self.connect.logger.warning('window_full_shot执行失败')
            a = traceback.format_exc()
            self.connect.logger.warning(a)

    def window_part_shot(self, pos1, pos2, file_name=None, gray=0):
        """
        窗口区域截图
        :param pos1: (x,y) 截图区域的左上角坐标
        :param pos2: (x,y) 截图区域的右下角坐标
        :param file_name: 截图文件的保存路径
        :param gray: 是否返回灰度图像，0：返回BGR彩色图像，其他：返回灰度黑白图像
        :return: file_name为空则返回RGB数据
        """
        w = pos2[0] - pos1[0]
        h = pos2[1] - pos1[1]
        hwindc = win32gui.GetWindowDC(self.connect.hwnd)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, w, h)
        memdc.SelectObject(bmp)
        memdc.BitBlt((self._offset_w, self._offset_h), (w - self._offset_w, h - self._offset_h), srcdc,
                     (pos1[0] + self._border_l, pos1[1] + self._border_t), win32con.SRCCOPY)

        if file_name is not None:
            bmp.SaveBitmapFile(memdc, file_name)
            srcdc.DeleteDC()
            memdc.DeleteDC()
            win32gui.ReleaseDC(self.connect.hwnd, hwindc)
            win32gui.DeleteObject(bmp.GetHandle())
            return
        else:
            signedIntsArray = bmp.GetBitmapBits(True)
            img = np.fromstring(signedIntsArray, dtype='uint8')
            img.shape = (h, w, 4)
            srcdc.DeleteDC()
            memdc.DeleteDC()
            win32gui.ReleaseDC(self.connect.hwnd, hwindc)
            win32gui.DeleteObject(bmp.GetHandle())
            if gray == 0:
                return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            else:
                return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    def find_img(self, img_template_path, part=0, pos1=None, pos2=None, gray=0):
        """
        查找图片
        :param img_template_path: 欲查找的图片路径
        :param part: 是否全屏查找，1为否，其他为是
        :param pos1: 欲查找范围的左上角坐标
        :param pos2: 欲查找范围的右下角坐标
        :param gray: 是否彩色查找，0：查找彩色图片，1：查找黑白图片
        :return: (maxVal,maxLoc) maxVal为相关性，越接近1越好，maxLoc为得到的坐标
        """
        # 获取截图
        if part == 1:
            img_src = self.window_part_shot(pos1, pos2, None, gray)
        else:
            img_src = self.window_full_shot(None, gray)

        # show_img(img_src)

        # 读入文件
        if gray == 0:
            img_template = cv2.imread(img_template_path, cv2.IMREAD_COLOR)
            template_h, template_w, _ = img_template.shape  # 模板图片的高度、长度
        else:
            img_template = cv2.imread(img_template_path, cv2.IMREAD_GRAYSCALE)
            template_h, template_w = img_template.shape  # 模板图片的高度、长度

        try:
            res = cv2.matchTemplate(
                img_src, img_template, cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
            maxLoc = (int(maxLoc[0] + template_w / 2), int(maxLoc[1] + template_h / 2))  # 计算中心坐标
            # print(maxLoc)
            return maxVal, maxLoc
        except Exception:
            self.connect.logger.warning('find_img执行失败')
            a = traceback.format_exc()
            self.connect.logger.warning(a)
            return 0, 0

    def find_and_click(self, img_template_path, confidence=0.5, offset_pos=(0, 0), gray=0):
        """
        查找图片并点击
        :param img_template_path: 欲查找的图片路径
        :param confidence: 置信度
        :param offset_pos: 偏移量，默认不偏移
        :param gray: 是否彩色查找，0：查找彩色图片，1：查找黑白图片
        :return:
        """
        conf, loc = self.find_img(img_template_path, 0, gray=gray)
        if conf >= confidence:
            click_pos = tuple(i + j for i, j in zip(loc, offset_pos))
            self.click_bg(click_pos)
        else:
            self.connect.logger.error('{} 查找失败'.format(img_template_path))
            self.take_screenshot()

    def take_screenshot(self):
        """
        截图
        """
        name = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        img_src_path = 'img/screenshots/{}.png'.format(name)
        self.window_full_shot(img_src_path)
        self.connect.logger.info('截图已保存至{}'.format(img_src_path))
        return img_src_path


class MuMuSimulator(Device):
    def __init__(self, name='MuMu模拟器'):
        super().__init__(name, ConnectEnum.MUMU.value)
        # MuMu模拟器上边黑条的偏移量 37px
        self._offset_h = -37
        # 实际高度需要去掉黑条偏移量
        self._client_h += self._offset_h


if __name__ == '__main__':
    mumu = MuMuSimulator('MuMu模拟器')
    mumu.find_img('')
