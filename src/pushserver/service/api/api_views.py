#coding:utf-8
__author__ = 'scott'

import os,datetime,time,traceback

from rest_framework.views import APIView
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import JSONParser,FormParser


from desert.errors import ErrorDefs
from desert.app import BaseAppServer
from desert.webservice.webapi import SuccCallReturn,FailCallReturn
from api_serializer import *
from model.core import models as core
from koala.koala_impl import Message_t
from mexs import mexs
from koala.base import *
from token import create_device_access_token

PAGE_SIZE = 100	#每次提交 page_size条记录，防止内存溢出


class RegisterView(APIView):
	"""
	app register
		应用程序注册推送服务客户端
		相同account的device根据platform类型仅存在一条记录，
			that is：  android客户端注册将覆盖前一次android客户端的注册记录
	:param :
		access_id - push_id
		secret_key - push_secret
		account   - 应用账号名称
		device_id - 设备编号
		platform  - 平台类型
		tag - 标签类型
	:return:
		access_token
	"""

	def post(self,request):
		cr = SuccCallReturn()
		serializer = RegisterSerializer(data=request.data)
		if not serializer.is_valid():
			cr = FailCallReturn(ErrorDefs.ParameterIllegal,serializer.errors)
			return cr.httpResponse()

		access_id = serializer.data['access_id']
		secret_key = serializer.data['secret_key']
		account = serializer.data['account']
		device_id = serializer.data['device_id']
		platform = serializer.data['platform']
		tag = serializer.data['tag']

		#添加或更新设备注册记录
		try:
			app = core.UserApplication.objects.get( access_id = access_id, secret_key = secret_key)
			rs = app.app_devices.filter( account = account , device_id = device_id )
			device = None
			if not rs:
				device = core.UserAppDevice()
			else:
				device = rs[0]
			device.app = app
			device.account = account
			device.device_id = device_id
			if tag:
				device.tag = tag
			if platform:
				device.platform = platform
			device.access_time = datetime.datetime.now()
			device.access_token = create_device_access_token()
			device.save()
			cr.assign( device.access_token )		# return device access_token to app

		except :
			cr = FailCallReturn(ErrorDefs.InternalException)
		return cr.httpResponse()


class MessageHelper:
	title = ''
	content = ''

	@classmethod
	def from_json(cls,data):
		return cls()
#
# class MessageView(APIView):
# 	"""
# 	message pushing
# 	:param APIView:
# 	:return:
# 	"""
# 	parser_classes = (JSONParser,)
#
# 	def simple(self,access_id,secret_key,data):
# 		"""
# 		simple()
# 			push simple text to all device
# 		:param data:
# 		 	title,content,platform
# 		:return:
# 		"""
# 		title = data['title']
# 		content = data['content']
# 		platform = data.get('platform',PlatformType.PLATFORM_UNDEFINE)
# 		platform = int(platform)
#
# 		message = Message_t()
# 		message.title = title
# 		message.content = content
#
# 		result = core.UserApplication.objects.get(access_id=access_id,secret_key=secret_key).app_devices.all()
# 		if platform:
# 			result = result.filter(platform = int(platform))
# 		self.sendMessagePaginated(result,message)
# 		return SuccCallReturn()
#
# 	def simple_device(self,access_id,secret_key,data):
# 		"""
# 		simple_device()
# 			push simple text to specified device
# 		:param data:
# 		 	device_token,title,content,platform
# 		:return:
# 		"""
# 		device_token = data['device_token']
# 		title = data['title']
# 		content = data['content']
# 		platform = data.get('platform',PlatformType.PLATFORM_UNDEFINE)
# 		platform = int(platform)
#
# 		message = Message_t()
# 		message.title = title
# 		message.content = content
#
# 		result = core.UserApplication.objects.get(access_id=access_id,secret_key=secret_key).app_devices.all()
# 		result = result.filter( access_token = device_token)
# 		if platform:
# 			result = result.filter(platform = int(platform))
# 		if result:
# 			r = result[0]
# 			token_list =[ device_token ]
# 			mexs.ServerApp.instance().sendMessage( token_list, message)
# 		return SuccCallReturn()
#
#
# 	def simple_account(self,access_id,secret_key,data):
# 		"""
# 		simple_acount
# 			push simple text to devices of account
# 		:param data:
# 		 	account,title,content,platform
# 		:return:
# 		"""
# 		account = data['account']
# 		title = data['title']
# 		content = data['content']
# 		platform = data.get('platform',PlatformType.PLATFORM_UNDEFINE)
# 		platform = int(platform)
#
# 		message = Message_t()
# 		message.title = title
# 		message.content = content
#
#
# 		result = core.UserApplication.objects.get(access_id=access_id,secret_key=secret_key).app_devices.all()
# 		if platform:
# 			result = result.filter(platform = int(platform))
# 		result = result.filter( account = account)
# 		self.sendMessagePaginated(result,message)
# 		return SuccCallReturn()
#
# 	def sendMessagePaginated(self,rs,message):
# 		"""
# 		sendMessagePaginated
# 			批量发送消息到目标设备
# 		:param rs:
# 		:param message:
# 		:return:
# 		"""
# 		page_index = 0
# 		result = rs
# 		while True:
# 			start = page_index * PAGE_SIZE
# 			end = start + PAGE_SIZE
# 			rs = result[ start: end ]
# 			if not rs:
# 				break
# 			token_list =[]
# 			for r in rs:
# 				token_list.append( r.access_token )	#设备授权凭证
# 			mexs.ServerApp.instance().sendMessage( token_list, message)
#
# 	def simple_tag(self,access_id,secret_key,data):
# 		"""
# 		simple_tag
# 			push simple text to  devices that be taged.
# 		:param data:
# 		 	tag,title,content,platform
# 		:return:
# 		"""
# 		tag = data['tag']
# 		title = data['title']
# 		content = data['content']
# 		platform = data.get('platform',PlatformType.P_UNDEFINED)
# 		platform = int(platform)
#
# 		message = Message_t()
# 		message.title = title
# 		message.content = content
#
#
# 		result = core.UserApplication.objects.get(access_id=access_id,secret_key=secret_key).app_devices.all()
# 		if platform:
# 			result = result.filter(platform = int(platform))
# 		result = result.filter( tag = tag)
# 		self.sendMessagePaginated(result,message)
# 		return SuccCallReturn()
#
# 	def post(self,request):
# 		"""
# 		post
# 			消息推送
# 		:param request:
# 			access_id,secret_key,method,detail...
# 		methods:
# 			simple,simple_device,simple_account,simple_tag  简单消息发送
# 			message,message_device,message_account,message_tag  复合消息发送
#
# 		:return:
# 		"""
# 		cr = SuccCallReturn()
# 		method = request.data['method']
# 		access_id = request.data['access_id']
# 		secret_key = request.data['secret_key']
#
# 		if hasattr(self,method):
# 			fx = getattr(self,method)
# 			try:
# 				cr = fx(access_id,secret_key,request.data)
# 			except:
# 				cr = FailCallReturn(ErrorDefs.InternalException)
# 		else:
# 			cr = FailCallReturn(ErrorDefs.ObjectNotExisted,'method not support: %s'%method)
# 		return cr.httpResponse()


@api_view(['POST'])
@parser_classes((JSONParser,))
def simple_all(request):
	"""
	simple()
		push simple text to all device
	:param data:
	    title,content,platform
	:return:
	"""
	cr = SuccCallReturn()
	access_id = request.data['access_id']
	secret_key = request.data['secret_key']
	data = request.data
	title = data['title']
	content = data['content']
	platform = data.get('platform',PlatformType.P_UNDEFINED)
	platform = int(platform)

	message = Message_t()
	message.title = title
	message.content = content

	result = core.UserApplication.objects.get(access_id=access_id,secret_key=secret_key).app_devices.all()
	if platform:
		result = result.filter(platform = int(platform))
	sendMessagePaginated(result,message)
	return cr.httpResponse()


@api_view(['POST'])
@parser_classes((FormParser,))
def simple_device(request):
	"""
	simple_device()
		push simple text to specified device
	:param data:
	    device_token,title,content,platform
	:return:
	"""
	cr = SuccCallReturn()

	access_id = request.data['access_id']
	secret_key = request.data['secret_key']
	data = request.data

	device_token = data['device_token']
	title = data['title']
	content = data['content']
	platform = data.get('platform',PlatformType.P_UNDEFINED)
	platform = int(platform)

	message = Message_t()
	message.title = title
	message.content = content

	app = core.UserApplication.objects.get(access_id=access_id,secret_key=secret_key)
	rs = app.app_devices.all()
	rs = rs.filter( access_token = device_token)
	if platform:
		rs = rs.filter(platform = int(platform))
	if rs:
		# r = result[0]
		token_list =[ device_token ]
		mexs.ServerAppMexs.instance().sendMessage( app.app_id, token_list, message)
	return cr.httpResponse()

@api_view(['POST'])
@parser_classes((JSONParser,))
def simple_account(request):
	"""
	simple_acount
		push simple text to devices of account
	:param data:
	    account,title,content,platform
	:return:
	"""
	cr = SuccCallReturn()
	access_id = request.data['access_id']
	secret_key = request.data['secret_key']
	data = request.data

	account = data['account']
	title = data['title']
	content = data['content']
	platform = data.get('platform',PlatformType.P_UNDEFINED)
	platform = int(platform)

	message = Message_t()
	message.title = title
	message.content = content


	result = core.UserApplication.objects.get(access_id=access_id,secret_key=secret_key).app_devices.all()
	if platform:
		result = result.filter(platform = int(platform))
	result = result.filter( account = account)
	sendMessagePaginated(result,message)
	return cr.httpResponse()

def sendMessagePaginated(rs,message,simple=True):
	"""
	sendMessagePaginated
		批量发送消息到目标设备
	:param rs:
	:param message:
	:return:
	"""
	page_index = 0
	result = rs

	start = page_index * PAGE_SIZE
	end = start + PAGE_SIZE
	while True:

		rs = result[ start: end ]
		if not rs:
			break
		start += PAGE_SIZE
		token_list =[]
		for r in rs:
			token_list.append( r.access_token )	#设备授权凭证

		mexs.ServerAppMexs.instance().sendMessage( token_list, message,simple)


@api_view(['POST'])
@parser_classes((JSONParser,))
def simple_tag(request):
	"""
	simple_tag
		push simple text to  devices that be taged.
	:param data:
	    tag,title,content,platform
	:return:
	"""
	cr = SuccCallReturn()
	access_id = request.data['access_id']
	secret_key = request.data['secret_key']
	data = request.data

	tag = data['tag']
	title = data['title']
	content = data['content']
	platform = data.get('platform',PlatformType.P_UNDEFINED)
	platform = int(platform)

	message = Message_t()
	message.title = title
	message.content = content


	result = core.UserApplication.objects.get(access_id=access_id,secret_key=secret_key).app_devices.all()
	if platform:
		result = result.filter(platform = int(platform))
	result = result.filter( tag = tag)
	sendMessagePaginated(result,message)
	return cr.httpResponse()

