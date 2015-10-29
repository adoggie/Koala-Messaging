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
elif os.path.exists('%s/../../common'%PATH):
	sys.path.append('%s/../../common'%PATH)
else:
	sys.path.append('%s/../../../common'%PATH)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import django
django.setup()	# 大坑呢 ,  django 1.8+版本必须加上一下代码行,不然出莫名错误
from django.contrib.auth.models import User

from model.core import models as core
from desert.misc import X,genUUID,getdigest
from koala.base import  PlatformType

USER_TYPE_ADMIN =1
USER_TYPE_NORMAL = 2

sf_auth_uri = 'https://login.salesforce.com/services/oauth2/authorize?response_type=code&client_id=3MVG9ZL0ppGP5UrBaWfLJxKHPpqFQHGY1G4ViJZxYd.GypuWOEfF_.BiAGwhHNUk1mB_KuJGdyWLT5kJvOHuh&redirect_uri=http%3a%2f%2flocalhost%3a8001%2foauth&state=first'


def_apps = [
	{'app_id':'com.test.first_app','app_name':'first application for testing','access_id':'c121e7d470bb11e5ab90ac87a316f916','secret_key':'shahaiNg1y',
	 'devices':[
		 {'device_id':'f5d2211170bb11e5ab9dac87a316f916','account':'test1@test.com','tag':'','access_token':getdigest(genUUID()),'platform':PlatformType.P_HTML5},
		 {'device_id':'7131251970bc11e5a52eac87a316f916','account':'test1@test.com','tag':'','access_token':getdigest(genUUID()),'platform':PlatformType.P_HTML5},
		 {'device_id':'78fcfe6670bc11e5bc41ac87a316f916','account':'test2@test.com','tag':'','access_token':getdigest(genUUID()),'platform':PlatformType.P_HTML5},
	 ]
	 },
]

def_users = [
	{'user_name':'scott','password':'111111','email':'first_app@test.com',
	 'apps':[
		 {'app_id':'com.test.first_app','app_name':'first application for testing','access_id':'c121e7d470bb11e5ab90ac87a316f916','secret_key':'shahaiNg1y',
	 		'devices':[
		 		{'device_id':'dev_id_0001','account':'test1@test.com','tag':'','access_token':'token_001','platform':PlatformType.P_HTML5},
		 		{'device_id':'dev_id_0002','account':'test2@test.com','tag':'','access_token':'token_002','platform':PlatformType.P_HTML5},
		 		{'device_id':'dev_id_0003','account':'test3@test.com','tag':'','access_token':'token_003','platform':PlatformType.P_HTML5},
	 		]
	 	}
	 ]}
]


def clearup():
	core.UserAppDevice.objects.all().delete()
	core.UserApplication.objects.all().delete()

	User.objects.filter(is_superuser=0).delete()

	for x in def_users:
		user = User.objects.create_user(x['user_name'],x['email'],x['password'])
		acc = core.PushUserAccount(user = user)
		acc.save()

		for en in x['apps']:
			app = core.UserApplication()
			app.account = acc
			app.app_id = en['app_id']
			app.app_name = en['app_name']
			app.is_active = True
			app.create_time = datetime.datetime.now()
			app.access_id = en['access_id']
			app.secret_key = en['secret_key']
			app.save()
			for dev in en['devices']:
				r = core.UserAppDevice()
				r.app = app
				r.device_id = dev['device_id']
				r.account = dev['account']
				r.tag = dev['tag']
				r.access_token = dev['access_token']
				r.access_time = datetime.datetime.now()
				r.platform = dev['platform']
				r.save()



def init_database():
	clearup()






if __name__ == "__main__":
	init_database()
