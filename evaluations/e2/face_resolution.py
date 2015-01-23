#! /usr/bin/env python

import cv2
import argparse
import numpy as np
import logging
import math


IMAGE = 'face_512x512.png'
TRAINING_DATA = 'lbpcascade_frontalface.xml'
SCALE_INCREMENT = .02

DETECT_SCALING_FACTOR = 1.1
NEIGHBORS_NEEDED = 2


logging.basicConfig(level=logging.INFO, format="%(message)s")


def read_image(image_name):
    
    image = cv2.imread(image_name)

    logging.info("Img W, Img H, Face W, Face H, Scale(%), Result")
    for scale in np.arange(1, 0, -SCALE_INCREMENT):

        scaled_image = cv2.resize(image, (0, 0), fx=scale, fy=scale)
        grey = cv2.cvtColor(scaled_image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier()
        face_cascade.load(TRAINING_DATA)
        faces = face_cascade.detectMultiScale(grey, DETECT_SCALING_FACTOR, NEIGHBORS_NEEDED)

        result = (len(faces) > 0)
        try:
            w, h = (faces[0][2], faces[0][3])
        except:
            w, h = (-1, -1)

        logging.info("%d, %d, %d, %d, %d, %s", 
            scaled_image.shape[0], scaled_image.shape[1], w, h, int(math.ceil(scale * 100)),
            "Found" if result else "Not Found")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find limits of resolution for face recognition")
    parser.add_argument('--image', default=IMAGE)
    args = parser.parse_args()
    read_image(args.image)
