#coding:utf-8
__author__ = 'scott'

from rest_framework.views import APIView
from rest_framework.decorators import api_view
import koala
from desert.errors import ErrorDefs

from desert.webservice.webapi import SuccCallReturn,FailCallReturn
from api_serializer import *

def RegisterView(APIView):
	"""
	app
	:param request:
	:return:
	"""

	def post(request):
		cr = SuccCallReturn()
		serializer = RegisterSerializer(data=request.data)
		if not serializer.is_valid(False):
			cr = FailCallReturn(ErrorDefs.ParameterIllegal,serializer.errors)

		return cr.httpResponse()





