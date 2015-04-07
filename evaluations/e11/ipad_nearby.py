#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import logging
import datetime
import time
import numpy as np


logging.basicConfig(level=logging.INFO, format="%(message)s")


def main():
    fixations = []
    with open('ipad_nearby_classification.txt', 'r') as ipad_file:
        last_time = datetime.datetime(1940, 1, 1, 1, 1, 1)
        visitor_start = last_time
        for line in ipad_file.readlines()[3:-1]:
            tokens = [_.strip() for _ in line.split('|')]
            time_ = time.strptime(tokens[1], '%Y-%m-%d %H:%M:%S')
            dt = datetime.datetime(time_.tm_year, time_.tm_mon, time_.tm_mday, 
                    time_.tm_hour, time_.tm_min, time_.tm_sec)
            if (dt - last_time).seconds > 15:
                time_passed = (last_time - visitor_start).seconds
                if time_passed > 0:
                    fixations.append(time_passed)
                visitor_start = dt
            last_time = dt
    return fixations


def stats(fixations):
    print "Avg: ", np.average(fixations)   
    print "Max: ", np.max(fixations)
    print "Med: ", np.median(fixations)
    print "Count: ", len(fixations)
    print "Sum: ", np.sum(fixations)


if __name__ == '__main__':
    fixations = main()
    stats(fixations)

