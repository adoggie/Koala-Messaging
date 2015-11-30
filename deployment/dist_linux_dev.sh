#!/bin/bash

# 发布服务代码到 deployment/services
# ** centos6.6 只能支持python2.6
# 代码拷贝到services之后，需要修改 settings.yaml和 service.xml内的主机ip地址

# centos => python 2.6.6 限制
# djangorestframework 3.2.4
# Python (2.6.5+, 2.7, 3.2, 3.3, 3.4)
# Django (1.5.6+, 1.6.3+, 1.7, 1.8)

# django 1.7 + 必须 python 2.7+


if [ $# == 0 ]; then
  echo 'error: dest dir need!'
  exit
fi

pwd=$(cd `dirname $0`;pwd)
#alias cp='cp -f'
alias rsync="rsync -rvt"


RELEASE_DIR=$(echo $1)
SRC_HOME=$pwd/..
KOALA_HOME=$RELEASE_DIR/koala

mkdir -p $KOALA_HOME
rsync -rvt  $SRC_HOME/common $KOALA_HOME

rsync -rvt  $SRC_HOME/src/* $KOALA_HOME
rsync -rvt  $pwd/../../TCE/python/tcelib $KOALA_HOME/common
rsync -rvt  $pwd/clean.sh $pwd/docker_start.sh $pwd/service_start.sh $pwd/init_db.sh $RELEASE_DIR
rsync -rvt  $pwd/scripts $RELEASE_DIR

#rm -r $KOALA_HOME/pushserver/koala.db


cat $SRC_HOME/common/etc/settings.yaml | sed 's/s100/localhost/' > $KOALA_HOME/common/etc/settings.yaml
cat $SRC_HOME/common/etc/services.xml | sed 's/s100/localhost/' > $KOALA_HOME/common/etc/services.xml