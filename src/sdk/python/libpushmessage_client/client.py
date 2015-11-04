#--coding:utf-8--

import os,os.path,sys,struct,time,traceback,time
# sys.path.insert(0,'../../../../python')

import urllib2,json,urllib

import gevent
import gevent.event


import tcelib as tce
from koala_imp import *


class TerminalImpl(ITerminal):
	def __init__(self):
		ITerminal.__init__(self)

	def onMessage(self,message,ctx):
		print 'onMessage:',message

	def onSystemNotification(self, notification, ctx):
		ITerminal.onSystemNotification(self, notification, ctx)

	def onSimpleText(self, text, ctx):
		ITerminal.onSimpleText(self, text, ctx)

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

		self.on_message = None
		self.ping = 5

		self.host = 'localhost'
		self.port = 16001
		self.ssl = False
		self.url = 'http://localhost/'

		self.reg_info = {}

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

		token = self.register(access_id,secret_key,account,device_id,tag,platform)
		if not token :
			return False

		ep = tce.RpcEndPoint(host= self.host,port=self.port,ssl = self.ssl)
		self.prx_mexs = IMessageServerPrx.create(ep)
		self.prx_gws = ITerminalGatewayServerPrx.create(ep)



		self.prx_gws.conn.setToken(token)

		adapter = tce.RpcCommAdapter('adapter')
		servant = TerminalImpl()
		adapter.addConnection( self.prx_gws.conn)
		adapter.addServant(servant)
		tce.RpcCommunicator.instance().addAdapter(adapter)

		gevent.spawn( self.thread_background )

		return True


	def thread_background(self):
		while True:
			print 'send Ping to gwserver..'
			self.prx_gws.ping_oneway()
			if not self.ev_wait.wait(self.ping):
				break

		print 'thread exiting..'


	def stop(self):
		pass

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
			'platfrom':platform
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

	def _on_message(self,title,content,extra = None):
		if self.on_message:
			self.on_message(title,content,extra)

def wait_for_shutdown():
	tce.waitForShutdown()




def message_recieved(title,content,extra):
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
	client.set_param('on_message',message_recieved)
	succ = client.open( ACCESS_ID,SECRET_KEY,ACCOUNT,DEVICE_ID,TAG,PLATFORM)
	print succ

	wait_for_shutdown()

def test_send_to_self():
	client.simple_text_account('aha!','nice day!',ACCOUNT) # send message to account specificed

if __name__ == '__main__':
	test_app()



