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

# MAIN
(
  # Lock ensures that this process is only running one at a time
  flock -x -w 1 200 || exit 1

  debug "Starting script"
  debug "Starting raspiyuv"

  raspiyuv\
    -w $W \
    -h $H \
    --timelapse 5000 \
    --timeout 0 \
    --nopreview \
    --colfx 128:128 \
    -o $DATADIR/image%04d.yuv &

  debug "raspiyuv started in background"
  debug "Entering processing loop"

  while ! test -f /tmp/stopsnap
  do
    sleep ${2:-2}s
    debug "Waking up to process files"
    for i in $DATADIR/*.yuv
    do
      if [[ $i == '*.yuv' ]]
      then
        debug "No new YUVs to process"
        continue
      fi
      debug "Processing yuv $i"
      res=`/usr/local/gallery/src/observer/./read_qr $i $W $H`
      debug "Result: $res"
      if [[ $res != '' ]]
      then
        echo "$res" >> $EVENTFILE
        /usr/local/gallery/src/observer/./upload.py $EVENTFILE
      fi
      debug "Deleting yuv $i"
      rm $i
    done
  done
) 200>/var/lock/.snap.lock 
