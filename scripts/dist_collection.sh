#!/bin/bash


# 发布服务代码到 deployment/services
# ** centos6.6 只能支持python2.6
# 代码拷贝到services之后，需要修改 settings.yaml和 service.xml内的主机ip地址

# centos => python 2.6.6 限制
# djangorestframework 3.2.4
# Python (2.6.5+, 2.7, 3.2, 3.3, 3.4)
# Django (1.5.6+, 1.6.3+, 1.7, 1.8)

# django 1.7 + 必须 python 2.7+

pwd=$(cd `dirname $0`;pwd)
alias cp='cp -f'

SERVICE_DIR=$pwd/../deployment/appbase/services
mkdir -p $SERVICE_DIR
cp -r $pwd/../common $SERVICE_DIR
cp -r $pwd/../src/* $SERVICE_DIR


cp -r $pwd/../../TCE/python/tcelib $SERVICE_DIR/common