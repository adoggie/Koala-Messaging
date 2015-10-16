__author__ = 'scott'

from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
	access_id = serializers.CharField(max_length= 100)  #app 注册编号
	secret_key = serializers.CharField(max_length= 40)  #app 登陆秘钥
	account = serializers.CharField(max_length= 40 )    #应用app的账号
	device_id = serializers.CharField(max_length= 100)  #应用app的设备编号
	platform = serializers.IntegerField() 		# 应用设备平台类型
	tag = serializers.CharField(max_length=40,required=False)  # app的设备标签

class SimpleMessageSerializer(serializers.Serializer):
	pass
	# serializers.
class MessageSerializer(serializers.Serializer):
	pass



