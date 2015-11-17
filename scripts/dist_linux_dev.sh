#!/bin/bash

pwd=$(cd `dirname $0`;pwd)
alias cp='cp -f'


SERVICE_DIR=$(echo $1)/services
mkdir -p $SERVICE_DIR
cp -r $pwd/../common $SERVICE_DIR
cp -r $pwd/../src/* $SERVICE_DIR
cp -r $pwd/../../TCE/python/tcelib $SERVICE_DIR/common
cp clean.sh docker_start.sh service_start.sh $1

#sed settings.yaml, service.xml

cat $pwd/../common/etc/settings.yaml | sed 's/s100/localhost/' > $SERVICE_DIR/common/etc/settings.yaml
cat $pwd/../common/etc/services.xml | sed 's/s100/localhost/' > $SERVICE_DIR/common/etc/services.xml