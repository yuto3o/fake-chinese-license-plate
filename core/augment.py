#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   augment.py
@License :   (C)Copyright 2020

@Modify Time        @Author    @Version    @Desciption
----------------    -------    --------    -----------
2020-07-01 16:59    yuyang     1.0         None
'''
# THIS FILE IS PART OF fakeCLP PROJECT


import numpy as np
import cv2
import random
import os


class Background:

    def __init__(self, width=1100, height=300):
        self.height = height
        self.width = width

        path = './source/background'
        self.paths = [os.path.join(path, name) for name in os.listdir(path)]

    def __call__(self):
        i = random.randint(0, len(self.paths) - 1)
        return cv2.resize(cv2.imread(self.paths[i]), (self.width, self.height))


def preprocess_image(image, size):
    """
    :param image: RGB, uint8
    :param size:
    :param bboxes:
    :return: RGB, uint8
    """
    iw, ih = size
    h, w, _ = image.shape

    scale = min(iw / w, ih / h)
    nw, nh = int(scale * w), int(scale * h)
    image_resized = cv2.resize(image, (nw, nh))

    image_paded = np.full(shape=[ih, iw, 3], dtype=np.uint8, fill_value=127)
    dw, dh = (iw - nw) // 2, (ih - nh) // 2
    image_paded[dh:nh + dh, dw:nw + dw, :] = image_resized

    return image_paded


def putPatchOn(src, background):
    canvas = np.zeros_like(background, dtype=background.dtype)
    h, w = src.shape[:2]
    bh, bw = background.shape[:2]

    canvas[:] = background[:]
    canvas[bh // 2 - h // 2:bh // 2 + h // 2, bw // 2 - w // 2:bw // 2 + w // 2] = src
    return canvas


def random_distort(image, hue=18, saturation=1.5, exposure=1.5):
    # determine scale factors
    dhue = np.random.uniform(-hue, hue)
    dsat = np.random.uniform(1. / saturation, saturation)
    dexp = np.random.uniform(1. / exposure, exposure)

    # convert RGB space to HSV space
    image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV).astype('float')

    # change satuation and exposure
    image[:, :, 1] *= dsat
    image[:, :, 2] *= dexp

    # change hue
    image[:, :, 0] += dhue

    image[:, :, 0] = np.clip(image[:, :, 0], 0., 179.)
    image[:, :, 1] = np.clip(image[:, :, 1], 0., 255.)
    image[:, :, 2] = np.clip(image[:, :, 2], 0., 255.)

    # convert back to RGB from HSV
    return cv2.cvtColor(image.astype('uint8'), cv2.COLOR_HSV2RGB)


def random_rotate(image, angle=5.):
    angle = np.random.uniform(-angle, angle)

    h, w, _ = image.shape
    m = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
    image = cv2.warpAffine(image, m, (w, h), borderMode=cv2.BORDER_REFLECT101)

    return image


def randon_crop_and_zoom(image, size, jitter=(0.05, 0.05)):
    net_w, net_h = size
    h, w, _ = image.shape
    dw = w * jitter[0]
    dh = h * jitter[1]

    rate = (w + np.random.uniform(-dw, dw)) / (h + np.random.uniform(-dh, dh))
    scale = np.random.uniform(1. / 1.15, 1.15)

    if (rate < 1):
        new_h = int(scale * net_h)
        new_w = int(new_h * rate)
    else:
        new_w = int(scale * net_w)
        new_h = int(new_w / rate)

    dx = int(np.random.uniform(0, (net_w - new_w)))
    dy = int(np.random.uniform(0, (net_h - new_h)))

    M = np.array([[new_w / w, 0., dx],
                  [0., new_h / h, dy]], dtype=np.float32)
    image = cv2.warpAffine(image, M, size, borderMode=cv2.BORDER_REPLICATE)

    return image


def _d(d, jitter=0.1):
    return d * random.uniform(-jitter, jitter)


def random_perspective(image):
    h, w, _ = image.shape
    point1 = np.array([[0, 0], [w, 0], [0, h], [w, h]], np.float32)
    point2 = np.array([[_d(w), _d(h)], [_d(w) + w, _d(h)], [_d(w), _d(h) + h], [_d(w) + w, _d(h) + h]], np.float32)

    m = cv2.getPerspectiveTransform(point1, point2)
    image = cv2.warpPerspective(image, m, (w, h), borderMode=cv2.BORDER_REPLICATE)

    return image


def random_blur(image, sigma=10):
    _sigma = random.randint(0, sigma)

    return cv2.GaussianBlur(image, (11, 11), _sigma)


_smu = cv2.imread('./source/noise/smu.jpg')


def random_add_smu(image):
    if random.randint(0, 1):
        rows = random.randint(0, _smu.shape[0] - image.shape[0])
        cols = random.randint(0, _smu.shape[1] - image.shape[1])
        add_smu = _smu[rows:rows + image.shape[0], cols:cols + image.shape[1]]
        image = cv2.bitwise_not(image)
        image = cv2.bitwise_and(add_smu, image)
        image = cv2.bitwise_not(image)
    return image
