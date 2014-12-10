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


''' Logging. '''
logging.basicConfig(
    filename='/var/log/gallery/snap.log', 
	level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M:%S'
)

''' Configurations. '''
LIGHTS_ENABLED = True
DETECTION_MODE = 'qr'
API_URL = "http://gallerypaths.com/api/sighting/"


def camLight(mode):
    ''' Toggle camera LED. '''
    led(27, mode)


def detectionLight(mode):
    ''' Toggle detection LED. '''
    led(17, mode)


def enablePin(index):
    subprocess.call(['gpio', '-g', 'mode', str(index), 'out'])


def led(index, mode):
    ''' Set an LED on or off. '''
    if mode == 'on' and LIGHTS_ENABLED:
        value = 1
    else:
        value = 0
    subprocess.call(['gpio', '-g', 'write', str(index), str(value)])


def takePics(cls, rotation, clientId, locationId):
    ''' Main program loop, takes pictures, processes, and uploads to server. '''

    netExecutor = ThreadPoolExecutor(max_workers = 3)

    with picamera.PiCamera() as camera:
        time.sleep(2)

        with picamera.array.PiRGBArray(camera) as stream:

            camera.rotation = rotation
            if cls == 'qr':
                camera.resolution = (1600, 900)
                camera.contrast = 50
                camera.brightness = 70
                stream = picamera.array.PiYUVArray(camera)
                format = 'yuv'
            elif cls == 'face':
                camera.resolution = (640, 480)
                face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
                stream = picamera.array.PiRGBArray(camera)
                format = 'bgr'

            ''' Main loop. '''
            startTime = time.time()
            for frame in camera.capture_continuous(stream, format=format, use_video_port=True):

                logging.info("New frame")           
                dt = datetime.datetime.utcnow()
                camLight('off')

                ''' Clear stream. '''
                stream.truncate()
                stream.seek(0)

                ''' Perform QR recognition. '''
                if cls == 'qr':
                    scanner = zbar.ImageScanner()
                    scanner.parse_config('enable')
                    zImg = zbar.Image(1600, 900, 'Y800', stream.getvalue())
                    scanner.scan(zImg)

                    hasSymbols = False
                    for symbol in zImg:
                        tl, bl, br, _ = [l for l in symbol.location]
                        logging.info("Found QR (%s) at %s, %s, %s", symbol.data, str(tl), str(bl), str(br))
                        netExecutor.submit(upload, dt, clientId, locationId, symbol.data, tl, bl, br)
                        hasSymbols = True

                    if hasSymbols:
                        detectionLight('on')
                    else:
                        detectionLight('off')

                ''' Perform face recognition. '''
                if cls == 'face':
                    image = stream.array
                    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(grey, 1.3, 5)

                    hasFaces = False
                    for (x, y, w, h) in faces:
                        tl = (x, y)
                        bl = (x, y + h)
                        br = (x + w, y + h)
                        logging.info("Found face at %s, %s, %s", str(tl), str(bl), str(br))
                        netExecutor.submit(upload, dt, clientId, locationId, '1024', tl, bl, br)
                        hasFaces = True

                    if hasFaces:
                        detectionLight('on')
                    else:
                        detectionLight('off')

                startTime = time.time()
                camLight('on')


def upload(dt, cId, lId, vId, tl, bl, br):
    ''' Upload detection event to server. '''
    try:
        visitorId = int(vId)
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
            headers={'Content-Type': 'application/json'})
        logging.info("Uploaded detection %s", json.dumps(detection))
    except:
        logging.warning("Could not upload request: %s",  json.dumps(detection))


def readConfig(configFilename):
    ''' Read observer configuration from file. '''
    config = ConfigParser.ConfigParser()
    config.readfp(open(configFilename))
    return config.get('observer', 'client_id'), config.get('observer', 'location_id')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="capture and process image stream")
    parser.add_argument("mode", help="face or qr")  # for now, we ignore this option
    parser.add_argument("-r", help="rotation", default=0)
    args = parser.parse_args()

    clientId, locationId = readConfig('/etc/observer.conf')
    logging.info("")
    logging.info("Client ID %s, Location ID %s", clientId, locationId)
    enablePin(17)
    enablePin(27)
    takePics(DETECTION_MODE, args.r, clientId, locationId)
