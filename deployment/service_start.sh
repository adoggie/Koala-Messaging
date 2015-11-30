#!/bin/bash

pwd=$(cd `dirname $0`;pwd)

bash $pwd/init_db.sh

nohup bash $pwd/scripts/gws.sh > /dev/null 2>&1 &
nohup bash $pwd/scripts/gws_websocket.sh > /dev/null 2>&1 &
nohup bash $pwd/scripts/server.sh > /dev/null 2>&1 &
while true
do
  read "enter into loop.."
done