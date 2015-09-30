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

def RegisterView(APIView):
	"""
	app register
	:param request:
	:return:
		access_token
	"""

	def post(request):
		cr = SuccCallReturn()
		serializer = RegisterSerializer(data=request.data)
		if not serializer.is_valid(False):
			cr = FailCallReturn(ErrorDefs.ParameterIllegal,serializer.errors)

		return cr.httpResponse()


class MessageWrapper:
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
		push simple text to all device
		:param data:
		:return:
		"""
		title = data['title']
		content = data['content']
		platform = data.get('platform')

		message = Message_t()
		message.title = title
		message.content = content

		#seek all records by paginating
		start = 0
		page_size = 100	#每次提交 page_size条记录，防止内存 exploded
		page_index = 0
		all = core.UserApplication.objects.get(access_id=access_id,secret_key=secret_key).app_devices.all().filter(platform = int(platform))
		while True:
			start = page_index * page_size
			end = start + page_size
			rs = all[ start: end]
			if not rs:
				break
			token_list =[]
			for r in rs:
				token_list.append( r.access_token )
			mexs.ServerApp.instance().sendMessage( token_list, message)

	def post(self,request):
		"""
		消息推送
		:param request:

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




