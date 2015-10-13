# -- coding:utf-8 --

"""
init_data.py
   初始化系统数据 ，模拟录入用户、应用和设备等记录
"""

import os
import sys,datetime

PATH = os.path.dirname(os.path.abspath(__file__))
if os.path.exists('%s/../common'%PATH):
	sys.path.append('%s/../common'%PATH)
else:
	sys.path.append('%s/../../common'%PATH)

import init_script



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from model.core import models as core
from desert.misc import X,genUUID,getdigest

USER_TYPE_ADMIN =1
USER_TYPE_NORMAL = 2

sf_auth_uri = 'https://login.salesforce.com/services/oauth2/authorize?response_type=code&client_id=3MVG9ZL0ppGP5UrBaWfLJxKHPpqFQHGY1G4ViJZxYd.GypuWOEfF_.BiAGwhHNUk1mB_KuJGdyWLT5kJvOHuh&redirect_uri=http%3a%2f%2flocalhost%3a8001%2foauth&state=first'


def_apps = [
	{'app_id':'com.test.first_app','app_name':'first application for testing','access_id':'c121e7d470bb11e5ab90ac87a316f916','secret_key':'shahaiNg1y',
	 'devices':[
		 {'device_id':'f5d2211170bb11e5ab9dac87a316f916','account':'test1@test.com','tag':'','access_token':'','platform':0},
		 {'device_id':'7131251970bc11e5a52eac87a316f916','account':'test1@test.com','tag':'','access_token':'','platform':0},
		 {'device_id':'78fcfe6670bc11e5bc41ac87a316f916','account':'test2@test.com','tag':'','access_token':'','platform':0},
	 ]
	 },
]


def clearup():
	core.UserAppDevice.objects.all().delete()
	core.UserApplication.objects.all().delete()


def init_database():
	clearup()






if __name__ == "__main__":
	init_database()
