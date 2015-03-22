#! /usr/bin/env python
# encoding: utf-8

import picamera
import picamera.array
import cv2


def takepic(res);
    with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as output:
            camera.resolution = res
            camera.capture(output, 'rgb')
            return output.array.copy()
