#!/bin/bash
# 
# Takes images once every 10 seconds and stores them in user-specified directory.
# Stops either by Ctrl-C or by touching a /tmp/stopsnap file.
# 
# Arguments:
# - $1: target directory for images
# - $2: time between consecutive snapshots (seconds)

DATADIR=${1:-"/usr/local/gallery/data"}
LOGFILE=/var/log/gallery/snap.log
EVENTFILE=$DATADIR/events.log
W=1600
H=960

function debug() {
  echo "[`date`]: $1" >> $LOGFILE
}

debug "Starting script"
debug "Starting raspiyuv"

raspiyuv\
  -w $W \
  -h $H \
  --timelapse 1000 \
  --nopreview \
  --timeout 0 \
  -o $DATADIR/image%09d.yuv &

debug "raspiyuv started in background"
debug "Entering processing loop"

while ! test -f /tmp/stopsnap
do
  sleep ${2:-20}s
  debug "Waking up to process files"
  for i in $DATADIR/*.yuv
  do
    debug "Processing yuv $i"
    res=`./read_qr $i $W $H`
    debug "Result: $res"
    if [[ $res != '' ]]
    then
      echo $res >> $EVENTFILE
    fi
    debug "Deleting yuv $i"
    rm $i
  done
done
