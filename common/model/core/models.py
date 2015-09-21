# coding=utf-8

"""
auth: sam
date: 2015/07/13
"""

from django.contrib.auth.models import User,UserManager

from django.db import models




class PushUserAccount(models.Model):
	user = models.OneToOneField(User,related_name='user_acct')



class UserApplication(models.Model):
	account = models.ForeignKey(PushUserAccount)
	app_id = models.CharField(max_length=200,unique=True,help_text=u'应用编号com.xyz.de')
	app_name = models.CharField(max_length=120,help_text=u'应用名称')
	is_active = models.BooleanField(help_text=u'是否可用')
	create_time = models.DateTimeField(help_text=u'创建时间')



if __name__ == '__main__':
	# print OrgUserAppConfig.app_auth_time.help_text
	pass
