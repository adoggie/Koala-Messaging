#!/bin/bash

pwd=$(cd `dirname $0`;pwd)

echo "initializing database..."
if [ ! -f $pwd/koala/pushserver/koala.db ];then
  python $pwd/koala/pushserver/project/manage.py syncdb --noinput
  python $pwd/koala/pushserver/project/init_data.py
  sleep 2
fi
