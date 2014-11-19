#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import argparse
import ConfigParser
import requests


API_URL='http://gallerypaths.com/api/sighting/'


def uploadDetections(detectionFilename, locationId, clientId):
    ''' Read detections from file and upload to server. '''
    for line in open(detectionFilename).readlines():
        data = line.split(',')
        detection = {
            'time': data[0],
            'client_id': clientId,
            'location_id': locationId,
            'visitor_id': int(data[1]),
            'x1': float(data[2]),
            'y1': float(data[3]),
            'x2': float(data[4]),
            'y2': float(data[5]),
            'x3': float(data[6]),
            'y3': float(data[7]),
        }
        print detection
        # requests.post(API_URL, data=json.dumps(detection), headers={'Content-Type': 'application/json'})


def readConfig(configFilename):
    ''' Read observer configuration from file. '''
    config = ConfigParser.ConfigParser()
    config.readfp(open(configFilename))
    return config.get('observer', 'client_id'), config.get('observer', 'location_id')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Upload visitor detection events to server")
    parser.add_argument('det_file', help="Text file with all detected events")
    parser.add_argument('-c', help="Observer configuration file", default="/etc/observer.conf")
    args = parser.parse_args()
    clientId, locationId = readConfig(args.c)
    uploadDetections(args.det_file, locationId, clientId)
