#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import argparse
import ConfigParser
import requests
import json


API_URL='http://gallerypaths.com/api/sighting/'


def uploadDetections(lines, locationId, clientId):
    ''' Read detections from file and upload to server. '''
    for line in lines:
        print "Uploading"
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
        try:
            requests.post(API_URL, data=json.dumps(detection), headers={'Content-Type': 'application/json'})
        except:
            print "Error posting detection to URL"


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

    ''' Fetch observer configuration. '''
    clientId, locationId = readConfig(args.c)

    ''' Upload lines of file to server. '''
    with open(args.det_file, 'r') as file_:
        lines = file_.readlines()
        lineCount = len(lines)
        uploadDetections(lines, locationId, clientId)

    ''' Delete all processed lines. 
        Leave all new lines added during execution. '''
    with open(args.det_file, 'r+') as file_:
        currentLines = file_.readlines()
        file_.seek(0)
        file_.truncate()
        if len(currentLines) > lineCount:
            file_.writelines(currentLines[lineCount:])
