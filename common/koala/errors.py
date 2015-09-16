#--coding:utf-8--


import os,os.path,sys,struct,time,traceback,signal,threading,datetime

from desert.errors import ErrorDefs as errdefs

class ErrorDefs:
	UserAnotherPlaceLogin = errdefs.InnerError(4001,u'未登录或会话过期')


