#--coding:utf-8--
"""
同步函数使用注意,不能令gevent线程挂起, 涉及: time.sleep,Thread ..
"""

import os,os.path,sys,struct,time,traceback,time

import urllib2,json,urllib

import gevent
import gevent.event

from koala_imp import *


class TerminalImpl(ITerminal):
	def __init__(self,app):
		ITerminal.__init__(self)
		self.app = app

	def onMessage(self,message,ctx):
		print 'onMessage:',message

	def onSystemNotification(self, notification, ctx):
		ITerminal.onSystemNotification(self, notification, ctx)

	def onSimpleText(self, text, ctx):
		ITerminal.onSimpleText(self, text, ctx)
		if self.app.on_simple_text:
			self.app.on_simple_text(text.title,text.content)

	def onError(self, errcode, errmsg, ctx):
		ITerminal.onError(self, errcode, errmsg, ctx)

class PlatformType:
	P_UNDEFINED = 0
	P_ANDROID = 1
	P_IOS = 2
	P_DESKTOP = 4
	P_HTML5 = 8


class PushMessageClient:
	def __init__(self):
		self.prx_mexs = None
		self.prx_gws = None

		self.ev_wait = gevent.event.Event()
		self.is_running = False

		self.on_message = None
		self.on_simple_text = None

		self.ping = 5

		self.host = 'localhost'
		self.port = 16001
		self.ssl = False
		self.url = 'http://localhost/'

		self.reg_info = {}
		self.token = None

		tce.RpcCommunicator.instance().init()


	_handle = None
	@classmethod
	def instance(cls):
		if not cls._handle:
			cls._handle = cls()
		return cls._handle

	def set_param(self,**kwargs):
		for key,value in kwargs.items():
			if hasattr(self,key):
				setattr(self,key,value)
		return self


	def open(self,access_id,secret_key,account,device_id,tag='',platform=0):
		ep = tce.RpcEndPoint(host= self.host,port=self.port,ssl = self.ssl)
		self.prx_mexs = IMessageServerPrx.create(ep)
		self.prx_gws = ITerminalGatewayServerPrx.create(ep)

		# self.register(access_id,secret_key,account,device_id,tag,platform)
		adapter = tce.RpcCommAdapter('adapter')
		servant = TerminalImpl(self)
		adapter.addConnection( self.prx_gws.conn)
		adapter.addServant(servant)
		tce.RpcCommunicator.instance().addAdapter(adapter)

		gevent.spawn( self.thread_background,reg_info={'access_id':access_id,
			'secret_key':secret_key,'account':account,'device_id':device_id,
			'tag':tag,'platform':platform
		} )


	def thread_background(self,reg_info):
		self.is_running = True
		access_id = reg_info['access_id']
		secret_key = reg_info['secret_key']
		account = reg_info['account']
		device_id = reg_info['device_id']
		tag = reg_info['tag']
		platform = reg_info['platform']

		while True:
			if not self.is_running:
				break
			if not self.token:
				self.register(access_id,secret_key,account,device_id,tag,platform)
			if self.token:
				print 'send Ping to gwserver..'
				self.prx_gws.ping_oneway()
			self.ev_wait.wait(self.ping)

		print 'background thread exiting..'


	def stop(self):
		self.token = None
		self.is_running = False
		self.ev_wait.set()

	def register(self,access_id,secret_key,account,device_id,tag,platform):
		"""

		:param access_id:
		:param secret_key:
		:param device_id:
		:param tag:
		:return:
			register-token
		"""
		params = {
			'access_id':access_id,
			'secret_key':secret_key,
			'account':account,
			'device_id':device_id,
			'tag':tag,
			'platform':platform
		}
		token = ''
		try:

			url = '%s/api/push/register/'%self.url.rstrip('/')
			res = urllib2.urlopen(url ,urllib.urlencode( params ))
			obj = json.loads(res.read())
			if obj.get('status',0)  in (0,'0'): # successful
				token = obj.get('result','')
			self.reg_info = params
		except:
			traceback.print_exc()
			self.reg_info = {}

		if token:
			self.prx_gws.conn.setToken(token)
			self.token = token
		return token

	def set_tag(self,tag):
		# push to server
		pass

	def simple_text(self,title,content,access_id=None,secret_key=None,platform=PlatformType.P_UNDEFINED):
		if not access_id:
			access_id = self.reg_info.get('access_id')
		if not secret_key:
			secret_key = self.reg_info.get('secret_key')
		params = {
			'access_id': access_id,
			'secret_key': secret_key,
			'title': title,
			'content': content,
			'platform': platform
		}

		result = False
		try:
			url = '%s/api/push/simple/all/'%self.url.rstrip('/')
			res = urllib2.urlopen(url ,urllib.urlencode( params ))
			obj = json.loads(res.read())
			if obj.get('status',0) not in (0,'0'): # successful
				result = True
		except:
			traceback.print_exc()
		return result

	def simple_text_device(self,title,content,token,access_id=None,secret_key=None,platform = PlatformType.P_UNDEFINED):
		if not access_id:
			access_id = self.reg_info.get('access_id')
		if not secret_key:
			secret_key = self.reg_info.get('secret_key')
		params = {
			'access_id': access_id,
			'secret_key': secret_key,
			'device_token': token,
			'title': title,
			'content': content,
			'platform':platform
		}

		result = False
		try:
			url = '%s/api/push/simple/device/'%self.url.rstrip('/')
			res = urllib2.urlopen(url ,urllib.urlencode( params ))
			obj = json.loads(res.read())
			if obj.get('status',0) not in (0,'0'): # successful
				result = True
		except:
			traceback.print_exc()
		return result

	def simple_text_account(self,title,content,account,access_id=None,secret_key=None,platform = PlatformType.P_UNDEFINED):
		if not access_id:
			access_id = self.reg_info.get('access_id')
		if not secret_key:
			secret_key = self.reg_info.get('secret_key')
		params = {
			'access_id': access_id,
			'secret_key': secret_key,
			'account': account,
			'title': title,
			'content': content,
			'platform':platform
		}

		result = False
		try:
			url = '%s/api/push/simple/account/'%self.url.rstrip('/')
			res = urllib2.urlopen(url ,urllib.urlencode( params ))
			obj = json.loads(res.read())
			if obj.get('status',0) not in (0,'0'): # successful
				result = True
		except:
			traceback.print_exc()
		return result

def wait_for_shutdown():
	tce.waitForShutdown()

def message_recieved(title,content,extra=None):
	print 'recved message:',title,content,extra

ACCESS_ID = '0098271772'
SECRET_KEY = 'qZmthanNk'
ACCOUNT = '14778920@163.com'
DEVICE_ID = 'c2RqZmthanNkZmtsYWpzZGtmbGphc2RmCg=='
TAG = 'cute'
PLATFORM = PlatformType.P_DESKTOP

client = None

def test_app():
	global client
	client = PushMessageClient()
	client.set_param(host='localhost',port=14001,ssl=False,url='http://localhost:16001')
	client.set_param(on_simple_text = message_recieved)
	client.open( ACCESS_ID,SECRET_KEY,ACCOUNT,DEVICE_ID,TAG,PLATFORM)

	gevent.spawn_later(2,test_send_to_self)	# 延后数秒,执行消息发送
	wait_for_shutdown()

def test_send_to_self():
	print client.token
	count = 1
	while True:
		# client.simple_text_account('boy!','times:< %s > nice gifts to you'%count,ACCOUNT) # send message to account specificed
		client.simple_text('boy!','times:< %s > nice gifts to you'%count) # send message to account specificed
		count+=1
		tce.sleep(3)
		# break

def test_send_lite():
	client = PushMessageClient()
	client.set_param(host='localhost',port=14001,ssl=False,url='http://localhost:16001')
	client.set_param(on_simple_text = message_recieved)
	for n in range(1000):
		client.simple_text_account('boy!','times:< %s > nice gifts to you'%n,ACCOUNT,access_id=ACCESS_ID,secret_key=SECRET_KEY) # send message to account specificed
		tce.sleep(2)

if __name__ == '__main__':
	# test_app()
	test_send_lite()



