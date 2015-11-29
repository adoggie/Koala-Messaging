#!/bin/bash

pwd=$(cd `dirname $0`;pwd)

nohup bash $pwd/scripts/gws.sh > /dev/null 2>&1 &
nohup bash $pwd/scripts/gws_websocket.sh > /dev/null 2>&1 &
nohup bash $pwd/scripts/server.sh > /dev/null 2>&1 &
