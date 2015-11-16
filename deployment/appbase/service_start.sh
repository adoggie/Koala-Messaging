#!/bin/bash
nohup python /opt/services/gws/server.py > /dev/null 2>&1 &
nohup python /opt/services/gws/server.py websocket > /dev/null 2>&1 &
nohup python /opt/services/pushserver/server.py > /dev/null 2>&1 &
