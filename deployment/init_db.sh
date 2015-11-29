#!/bin/bash

pwd=$(cd `dirname $0`;pwd)

echo "initializing database..."
python $pwd/koala/pushserver/project/init_data.py
sleep 2
