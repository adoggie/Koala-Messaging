#!/usr/bin/env bash

#mkdir /home/koala
pwd=$(cd `dirname $0`;pwd)
DEAMON=-d
VER=$1
docker run --name koala $DEAMON -it -v $pwd:/opt -p 25432:5432 -p 37017:37017 -p 16379:6379 -p 15672:5672 -p 16001:16001 -p 20080:80 -p 14001:14001 -p 14002:14002 koala:0.0.4 /run/start_koala.sh
