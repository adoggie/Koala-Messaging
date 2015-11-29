#!/bin/bash

pwd=$(cd `dirname $0`;pwd)
KOALA=$pwd/koala

python $KOALA/pushserver/server.py > /dev/null 2>&1 &
