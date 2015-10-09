#coding:utf-8
__author__ = 'scott'

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from koala.koala_impl import Message_t
from desert.errors import ErrorDefs
from desert.app import BaseAppServer
from desert.webservice.webapi import SuccCallReturn,FailCallReturn
from api_serializer import *
from model.core import models as core
from mexs import mexs
from koala.base import *

PAGE_SIZE = 100	#每次提交 page_size条记录，防止内存溢出


def RegisterView(APIView):
	"""
	app register
	:param request:
		access_id - push_id
		secret_key - push_secret
		account   - 应用账号名称
		device_id - 设备编号
		platform  - 平台类型
	:return:
		access_token
	"""

	def post(request):
		cr = SuccCallReturn()
		serializer = RegisterSerializer(data=request.data)
		if not serializer.is_valid(False):
			cr = FailCallReturn(ErrorDefs.ParameterIllegal,serializer.errors)

		return cr.httpResponse()


class MessageHelper:
	title = ''
	content = ''

	@classmethod
	def from_json(cls,data):
		return cls()

def MessageView(APIView):
	"""
	message pushing
	:param APIView:
	:return:
	"""
	parser_classes = (JSONParser,)

	def simple(self,access_id,secret_key,data):
		"""
		simple()
			push simple text to all device
		:param data:
		 	title,content,platform
		:return:
		"""
		title = data['title']
		content = data['content']
		platform = data.get('platform',PlatformType.PLAT_UNDEFINE)
		platform = int(platform)

		message = Message_t()
		message.title = title
		message.content = content

		page_index = 0
		result = core.UserApplication.objects.get(access_id=access_id,secret_key=secret_key).app_devices.all()
		if platform:
			result = result.filter(platform = int(platform))

		while True:
			start = page_index * PAGE_SIZE
			end = start + PAGE_SIZE
			rs = result[ start: end ]
			if not rs:
				break
			token_list =[]
			for r in rs:
				token_list.append( r.access_token )	#设备授权凭证
			mexs.ServerApp.instance().sendMessage( token_list, message)

	def simple_device(self,access_id,secret_key,data):
		"""
		simple_device()
			push simple text to specified device
		:param data:
		 	device_token,title,content,platform
		:return:
		"""
		device_token = data['device_token']
		title = data['title']
		content = data['content']
		platform = data.get('platform',PlatformType.PLAT_UNDEFINE)
		platform = int(platform)

		message = Message_t()
		message.title = title
		message.content = content

		page_index = 0
		result = core.UserApplication.objects.get(access_id=access_id,secret_key=secret_key).app_devices.all()
		result = result.filter( access_token = device_token)
		if platform:
			result = result.filter(platform = int(platform))
		if result:
			r = result[0]
			token_list =[ device_token ]
			mexs.ServerApp.instance().sendMessage( token_list, message)

	def post(self,request):
		"""
		post
			消息推送
		:param request:
			access_id,secret_key,method,detail...
		methods:
			simple,simple_device,simple_account,simple_tag  简单消息发送
			message,message_device,message_account,message_tag  复合消息发送

		:return:
		"""
		cr = SuccCallReturn()
		method = request.data['method']
		access_id = request.data['access_id']
		secret_key = request.data['secret_key']

		if hasattr(self,method):
			fx = getattr(self,method)
			cr = fx(access_id,secret_key,request.data)
		else:
			cr = FailCallReturn(ErrorDefs.ObjectNotExisted,'method not support: %s'%method)
		return cr




