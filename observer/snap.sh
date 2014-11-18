#!/bin/bash
# 
# Takes images once every 10 seconds and stores them in user-specified directory.
# Stops either by Ctrl-C or by touching a /tmp/stopsnap file.
# 
# Arguments:
# - $1: target directory for images
# - $2: time between consecutive snapshots

while ! test -f /tmp/stopsnap
do
  raspistill\
    --nopreview \
    --timeout 500 \
    -o ${1:-"/tmp"}/`date --utc +%FT%TZ`.jpg
  sleep ${2:-10}
done
