#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   utils.py
@License :   (C)Copyright 2020

@Modify Time        @Author    @Version    @Desciption
----------------    -------    --------    -----------
2020-07-01 15:12    yuyang     1.0         None
'''
# THIS FILE IS PART OF fakeCLP PROJECT

import cv2
import numpy as np


def cv_imread(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)


def cv_imwrite(filename, src):
    cv2.imencode('.jpg', src)[1].tofile(filename)
