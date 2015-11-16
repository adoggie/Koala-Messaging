#!/bin/bash


#发布服务代码到 deployment/services

pwd=$(cd `dirname $0`;pwd)
alias cp='cp -f'

SERVICE_DIR=$pwd/../deployment/appbase/services
mkdir -p $SERVICE_DIR
cp -r $pwd/../common $SERVICE_DIR
cp -r $pwd/../src/* $SERVICE_DIR
