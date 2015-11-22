# coding=utf-8

"""
auth: sam
date: 2015/07/13
"""

from django.contrib.auth.models import User,UserManager

from django.db import models
import django.db.models




class PushUserAccount(models.Model):
	user = models.OneToOneField(User,related_name='auth_user')




class UserApplication(models.Model):
	account = models.ForeignKey(PushUserAccount,related_name='user_apps')
	app_id = models.CharField(max_length=200,unique=True,help_text=u'应用编号com.xyz.de')
	app_name = models.CharField(max_length=120,help_text=u'应用名称')
	is_active = models.BooleanField(help_text=u'是否可用')
	create_time = models.DateTimeField(help_text=u'创建时间')
	access_id = models.CharField(max_length=200,unique=True,db_index=True,help_text=u'应用访问标识')
	secret_key = models.CharField(max_length=200,db_index=True,help_text=u'应用访问秘钥')
	address_restricted = models.BooleanField(default=False,help_text=u'消息推送者的ip地址限制')

	class Meta:
		index_together = ( ("access_id", "secret_key"),)

class UserAppDevice(models.Model):
	"""
	device 描述一个app应用登陆的设备
	"""
	app = models.ForeignKey(UserApplication,db_index=True,related_name='app_devices',on_delete= django.db.models.CASCADE)
	device_id = models.CharField(max_length=100,db_index=True,help_text=u'设备编号')
	account = models.CharField(max_length=40,db_index=True,help_text=u'app应用的用户账号')
	tag = models.CharField(max_length=40,db_index=True,null=True,help_text=u'设备标签')
	access_token = models.CharField(max_length=200,null=True,help_text=u'设备登陆访问token')
	access_time = models.DateTimeField(null=True,help_text=u'最近一次访问时间')
	platform = models.SmallIntegerField(help_text=u'平台类型')

class PushAddressRestricted(models.Model):
	"""
	消息推送请求的ip地址限制
	"""
	app = models.ForeignKey(UserApplication,related_name='address_restricted_set',on_delete= django.db.models.CASCADE)
	name = models.CharField(max_length=40)
	address = models.CharField(max_length=40,help_text=u'访问地址')
	mask = models.SmallIntegerField(default=0,help_text=u'地址掩码')
	comment = models.CharField(max_length=200,null=True,default='')
	is_black = models.BooleanField(default=False,help_text=u'是否是黑名单')
	is_active = models.BooleanField(default=True,help_text=u'是否启用')



if __name__ == '__main__':
	# print OrgUserAppConfig.app_auth_time.help_text
	pass
