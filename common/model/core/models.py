# coding=utf-8

"""
auth: sam
date: 2015/07/13
"""

from django.contrib.auth.models import User,UserManager

from django.db import models




class PushUserAccount(models.Model):
	user = models.OneToOneField(User,related_name='auth_user')




class UserApplication(models.Model):
	account = models.ForeignKey(PushUserAccount)
	app_id = models.CharField(max_length=200,unique=True,help_text=u'应用编号com.xyz.de')
	app_name = models.CharField(max_length=120,help_text=u'应用名称')
	is_active = models.BooleanField(help_text=u'是否可用')
	create_time = models.DateTimeField(help_text=u'创建时间')
	access_id = models.CharField(max_length=200,unique=True,db_index=True,help_text=u'应用访问标识')
	secret_key = models.CharField(max_length=200,db_index=True,help_text=u'应用访问秘钥')

	class Meta:
		index_together = ( ("access_id", "secret_key"),)

class UserAppDevice(models.Model):
	"""
	device 描述一个app应用登陆的设备
	"""
	app = models.ForeignKey(UserApplication,db_index=True,related_name='app_devices')
	device_id = models.CharField(max_length=100,db_index=True,help_text=u'设备编号')
	account = models.CharField(max_length=40,db_index=True,help_text=u'app应用的用户账号')
	tag = models.CharField(max_length=40,db_index=True,null=True,help_text=u'设备标签')
	access_token = models.CharField(max_length=200,null=True,help_text=u'设备登陆访问token')
	access_time = models.DateTimeField(null=True,help_text=u'最近一次访问时间')
	platform = models.SmallIntegerField(help_text=u'平台类型')

if __name__ == '__main__':
	# print OrgUserAppConfig.app_auth_time.help_text
	pass
