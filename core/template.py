#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   template
@License :   (C)Copyright 2020

@Modify Time        @Author    @Version    @Desciption
----------------    -------    --------    -----------
2020-07-01 14:04    yuyang     1.0         None
'''
# THIS FILE IS PART OF fakeCLP PROJECT

import numpy as np
import random
import cv2
import os
import re

from core.common import *
from core.utils import *


class Plate:

    def __init__(self):
        pass

    def __call__(self):
        raise NotImplementedError()

    def getCharImg(self, char, size):
        raise NotImplementedError()

    def getRandomCode(self, num=5):
        p = random.randint(0, 2)
        c = ''

        for _ in range(num - p):
            c += random.choice(NumberChar)

        for _ in range(p):
            c += random.choice(AlphabetChar)

        c = list(c)
        random.shuffle(c)
        c = ''.join(c)

        return c

    def getRandomCode_balance(self, num=5):
        c = ''

        for _ in range(num):
            c += random.choice(NumberChar + AlphabetChar)

        c = list(c)
        random.shuffle(c)
        c = ''.join(c)

        return c


class Blue440x140(Plate):

    def __init__(self):
        super().__init__()

        self.lp_height = 280
        self.lp_width = 880

        self.ch_height = 180
        self.ch_width = 90

        self.up_interval = 50
        self.left_interval = 45
        self.ch_interval = 24
        self.point_size = 20

        font_name = os.listdir('./source/font')
        font = [n for n in font_name if n.startswith('140')]
        self.fonts = {re.findall(r"_(.?).jpg", f)[0]: cv2.resize(cv_imread(os.path.join('./source/font', f)),
                                                                 ((self.ch_width, self.ch_height))) for f in font}
        self.template = cv2.resize(cv_imread('./source/plate/blue_140.PNG'), (self.lp_width, self.lp_height))[..., :3]

    def getCharImg(self, char, size):
        char_img = self.fonts[char]
        return cv2.resize(char_img, size)

    def __call__(self, *args, **kwargs):
        prov = ProvinceChar.keys()
        _prov = random.choice(list(prov))
        _city = random.choice(ProvinceChar[_prov])
        _code = self.getRandomCode(num=5)
        code = _prov + _city + _code

        img = np.ones((self.lp_height, self.lp_width, 3), dtype=np.uint8) * 255

        char_width_start = self.left_interval
        char_width_end = char_width_start + self.ch_width
        char_height_start = self.up_interval
        char_height_end = char_height_start + self.ch_height
        img[char_height_start:char_height_end, char_width_start:char_width_end] = self.getCharImg(code[0], (
        self.ch_width, self.ch_height))

        char_width_start = char_width_end + self.ch_interval
        char_width_end = char_width_start + self.ch_width
        img[char_height_start:char_height_end, char_width_start:char_width_end] = self.getCharImg(code[1], (
        self.ch_width, self.ch_height))

        char_width_end = char_width_end + self.point_size

        for i in range(2, 7):
            char_width_start = char_width_end + self.ch_interval
            char_width_end = char_width_start + self.ch_width
            img[char_height_start:char_height_end, char_width_start:char_width_end] = self.getCharImg(code[i], (
            self.ch_width, self.ch_height))

        return code, cv2.bitwise_or(~img, self.template)


class Yellow440x140(Plate):

    def __init__(self):
        super().__init__()

        self.lp_height = 280
        self.lp_width = 880

        self.ch_height = 180
        self.ch_width = 90

        self.up_interval = 50
        self.left_interval = 45
        self.ch_interval = 24
        self.point_size = 20

        font_name = os.listdir('./source/font')
        font = [n for n in font_name if n.startswith('140')]
        self.fonts = {re.findall(r"_(.?).jpg", f)[0]: cv2.resize(cv_imread(os.path.join('./source/font', f)),
                                                                 ((self.ch_width, self.ch_height))) for f in font}
        self.template = cv2.resize(cv_imread('./source/plate/yellow_140.PNG'), (self.lp_width, self.lp_height))[..., :3]

    def getCharImg(self, char, size):
        char_img = self.fonts[char]
        return cv2.resize(char_img, size)

    def __call__(self, *args, **kwargs):
        prov = ProvinceChar.keys()
        _prov = random.choice(list(prov))
        _city = random.choice(ProvinceChar[_prov])
        _code = self.getRandomCode(num=5)
        code = _prov + _city + _code

        img = np.ones((self.lp_height, self.lp_width, 3), dtype=np.uint8) * 255

        char_width_start = self.left_interval
        char_width_end = char_width_start + self.ch_width
        char_height_start = self.up_interval
        char_height_end = char_height_start + self.ch_height
        img[char_height_start:char_height_end, char_width_start:char_width_end] = self.getCharImg(code[0], (
        self.ch_width, self.ch_height))

        char_width_start = char_width_end + self.ch_interval
        char_width_end = char_width_start + self.ch_width
        img[char_height_start:char_height_end, char_width_start:char_width_end] = self.getCharImg(code[1], (
        self.ch_width, self.ch_height))

        char_width_end = char_width_end + self.point_size

        for i in range(2, 7):
            char_width_start = char_width_end + self.ch_interval
            char_width_end = char_width_start + self.ch_width
            img[char_height_start:char_height_end, char_width_start:char_width_end] = self.getCharImg(code[i], (
            self.ch_width, self.ch_height))

        return code, cv2.bitwise_and(img, self.template)


class Yellow440x220(Plate):

    def __init__(self):
        super().__init__()

        self.lp_height = 440
        self.lp_width = 880

        self.up_interval = 30
        self.up_ch_height = 120
        self.up_ch_width = 160
        self.up_ch_interval = 50
        self.up_point_size = 20
        self.up_left_interval = 220

        self.interval = 30
        self.dw_ch_height = 220
        self.dw_ch_width = 130
        self.dw_ch_interval = 30
        self.dw_left_interval = 55

        font_name = os.listdir('./source/font')
        font1 = [n for n in font_name if n.startswith('220_up')]
        self.up_fonts = {re.findall(r"_(.?).jpg", f)[0]: cv2.resize(cv_imread(os.path.join('./source/font', f)),
                                                                 ((self.up_ch_width, self.up_ch_height))) for f in font1}

        font2 = [n for n in font_name if n.startswith('220_down')]
        self.dw_fonts = {re.findall(r"_(.?).jpg", f)[0]: cv2.resize(cv_imread(os.path.join('./source/font', f)),
                                                                 ((self.up_ch_width, self.up_ch_height))) for f in font2}

        font = [n for n in font_name if n not in font1 and n not in font2]
        self.fonts = {re.findall(r"_(.?).jpg", f)[0]: cv2.resize(cv_imread(os.path.join('./source/font', f)),
                                                                 ((self.up_ch_width, self.up_ch_height))) for f in font}

        self.up_fonts.update(self.fonts)
        self.dw_fonts.update(self.fonts)

        self.template = cv2.resize(cv_imread('./source/plate/yellow_220.PNG'), (self.lp_width, self.lp_height))[..., :3]

    def getCharImg(self, char, size):
        char_img = self.fonts[char]
        return cv2.resize(char_img, size)

    def __call__(self, *args, **kwargs):
        prov = ProvinceChar.keys()
        _prov = random.choice(list(prov))
        _city = random.choice(ProvinceChar[_prov])
        _code = self.getRandomCode(num=5)
        code = _prov + _city + _code

        img = np.ones((self.lp_height, self.lp_width, 3), dtype=np.uint8) * 255

        self.fonts = self.up_fonts
        char_width_start = self.up_left_interval
        char_width_end = char_width_start + self.up_ch_width
        char_height_start = self.up_interval
        char_height_end = char_height_start + self.up_ch_height
        img[char_height_start:char_height_end, char_width_start:char_width_end] = self.getCharImg(code[0], (
        self.up_ch_width, self.up_ch_height))

        char_width_start = char_width_end + self.up_ch_interval + self.up_point_size + self.up_ch_interval
        char_width_end = char_width_start + self.up_ch_width
        img[char_height_start:char_height_end, char_width_start:char_width_end] = self.getCharImg(code[1], (
        self.up_ch_width, self.up_ch_height))

        self.fonts = self.dw_fonts
        char_width_start = self.dw_left_interval
        char_width_end = char_width_start + self.dw_ch_width
        char_height_start = char_height_end + self.interval
        char_height_end = char_height_start + self.dw_ch_height

        for i in range(2, 7):
            img[char_height_start:char_height_end, char_width_start:char_width_end] = self.getCharImg(code[i], (
            self.dw_ch_width, self.dw_ch_height))

            char_width_start = char_width_end + self.dw_ch_interval
            char_width_end = char_width_start + self.dw_ch_width

        return code, cv2.bitwise_and(img, self.template)


class Green480x140(Plate):

    def __init__(self):
        super().__init__()

        self.lp_height = 280
        self.lp_width = 960

        self.ch_height = 180
        self.ch_width = 90

        self.up_interval = 50
        self.left_interval = 35
        self.ch_interval = 18
        self.point_size = 60

        font_name = os.listdir('./source/font')
        font = [n for n in font_name if n.startswith('green')]
        self.fonts = {re.findall(r"_(.?).jpg", f)[0]: cv2.resize(cv_imread(os.path.join('./source/font', f)),
                                                                 ((self.ch_width, self.ch_height))) for f in font}
        self.template = cv2.resize(cv_imread('./source/plate/green_car_140.PNG'), (self.lp_width, self.lp_height))[...,
                        :3]

    def getCharImg(self, char, size):
        char_img = self.fonts[char]
        return cv2.resize(char_img, size)

    def __call__(self, *args, **kwargs):
        prov = ProvinceChar.keys()
        _prov = random.choice(list(prov))
        _city = random.choice(ProvinceChar[_prov])
        _code = self.getRandomCode(num=6)
        code = _prov + _city + _code

        img = np.ones((self.lp_height, self.lp_width, 3), dtype=np.uint8) * 255

        char_width_start = self.left_interval
        char_width_end = char_width_start + self.ch_width
        char_height_start = self.up_interval
        char_height_end = char_height_start + self.ch_height
        img[char_height_start:char_height_end, char_width_start:char_width_end] = self.getCharImg(code[0], (
        self.ch_width, self.ch_height))

        char_width_start = char_width_end + self.ch_interval
        char_width_end = char_width_start + self.ch_width
        img[char_height_start:char_height_end, char_width_start:char_width_end] = self.getCharImg(code[1], (
        self.ch_width, self.ch_height))

        char_width_end = char_width_end + self.point_size

        for i in range(2, 8):
            char_width_start = char_width_end + self.ch_interval
            char_width_end = char_width_start + self.ch_width
            img[char_height_start:char_height_end, char_width_start:char_width_end] = self.getCharImg(code[i], (
            self.ch_width, self.ch_height))

        return code, cv2.bitwise_and(img, self.template)
