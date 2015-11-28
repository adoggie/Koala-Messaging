#--coding:utf-8--


import os,os.path,sys,struct,time,traceback,signal,threading,datetime

from desert.errors import ErrorDefs as errdefs

class ErrorDefs:
	UserAnotherPlaceLogin = errdefs.InnerError(4001,u'未登录或会话过期')
	PushReject_AddressRestricted = errdefs.InnerError(5001,u'消息推送禁止(发送者地址受限)')


