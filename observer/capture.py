#! /usr/bin/env python

import argparse
import logging
import sys
import time
import datetime
import os
import subprocess
import ConfigParser
import json
import requests
from concurrent.futures import ThreadPoolExecutor

import picamera
import picamera.array
import cv2
import zbar
from detect import FaceRecognizer


''' Logging. '''
logging.basicConfig(
    filename='/var/log/gallery/snap.log', 
	level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M:%S'
)

''' Configurations. '''
LIGHTS_ENABLED = True
DETECTION_MODE = 'face'
API_URL = "https://gallerypaths.com/api/sighting/"


def cam_light(mode):
    ''' Toggle camera LED. '''
    led(27, mode)


def detection_light(mode):
    ''' Toggle detection LED. '''
    led(17, mode)


def enable_pin(index):
    subprocess.call(['gpio', '-g', 'mode', str(index), 'out'])


def led(index, mode):
    ''' Set an LED on or off. '''
    if mode == 'on' and LIGHTS_ENABLED:
        value = 1
    else:
        value = 0
    subprocess.call(['gpio', '-g', 'write', str(index), str(value)])


""" MAIN PROCEDURES. """

def takePics(cls, rotation, client_id, location_id):
    ''' Main program loop, takes pictures, processes, and uploads to server. '''

    net_executor = ThreadPoolExecutor(max_workers = 3)
    recognizer = FaceRecognizer(decay=30)

    with picamera.PiCamera() as camera:
        time.sleep(2)

        with picamera.array.PiRGBArray(camera) as stream:

            camera.rotation = rotation
            camera.resolution = (640, 480)
            stream = picamera.array.PiRGBArray(camera)
            format = 'bgr'

            ''' Main loop. '''
            start_time = time.time()
            for frame in camera.capture_continuous(stream, format=format, use_video_port=True):

                logging.info("New frame")
                dt = datetime.datetime.utcnow()
                cam_light('off')

                ''' Clear stream. '''
                stream.truncate()
                stream.seek(0)

                ''' Perform face recognition. '''
                image = stream.array
                faces = recognizer.find_faces(image)

                ''' Report faces to server. '''
                hasFaces = False
                for (x, y, w, h, vi) in faces:
                    tl = (x, y)
                    bl = (x, y + h)
                    br = (x + w, y + h)
                    logging.info("Found face %s at %s, %s, %s", str(vi), str(tl), str(bl), str(br))
                    net_executor.submit(upload, dt, client_id, location_id, vi, tl, bl, br)
                    hasFaces = True

                if hasFaces:
                    detection_light('on')
                else:
                    detection_light('off')

                start_time = time.time()
                cam_light('on')


def upload(dt, cId, lId, vId, tl, bl, br):
    ''' Upload detection event to server. '''
    try:
        visitor_id = int(vId)
    except:
        logging.warning("Skipping invalid visitor ID: %s", str(vId))
        return

    detection = {
        'time': str(dt),
        'client_id': cId,
        'location_id': lId,
        'visitor_id': vId,
        'x1': float(tl[0]),
        'y1': float(tl[1]),
        'x2': float(bl[0]),
        'y2': float(bl[1]),
        'x3': float(br[0]),
        'y3': float(br[1]),
    }
    try:
        requests.post(API_URL, data=json.dumps(detection), 
            headers={'Content-Type': 'application/json'}, verify=False)
        logging.info("Uploaded detection %s", json.dumps(detection))
    except:
        logging.warning("Could not upload request: %s",  json.dumps(detection))


def readConfig(config_filename):
    ''' Read observer configuration from file. '''
    config = ConfigParser.ConfigParser()
    config.readfp(open(config_filename))
    return config.get('observer', 'client_id'), config.get('observer', 'location_id')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="capture and process image stream")
    parser.add_argument("mode", help="face or qr")  # for now, we ignore this option
    parser.add_argument("-r", help="rotation", default=0)
    args = parser.parse_args()

    client_id, location_id = readConfig('/etc/observer.conf')
    logging.info("")
    logging.info("Client ID %s, Location ID %s", client_id, location_id)
    enable_pin(17)
    enable_pin(27)
    takePics(DETECTION_MODE, 0, client_id, location_id)
