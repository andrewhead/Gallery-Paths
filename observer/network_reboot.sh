#! /bin/bash
# Reboot network interfaces on this board if network is down.
# Run with sudo permissions.

SERVER_URL="www.gallerypaths.com"
LOG_FILE=/var/log/gallery/network

curl $SERVER_URL
if [ $? -ne 0 ]
then
  echo "[`date`] Internet down.  Rebooting..." >> $LOG_FILE
  ifdown wlan0; sleep 5s; ifup wlan0;
else
  echo "[`date`] Internet still up!" >> $LOG_FILE
fi
