#--coding:utf-8--


'''
	mexs - 消息交换服务器
		提供消息投递、转发、通知功能
	author: mark
	date:   2014.3.20

	目前仅考虑单点设备登录
'''

import os,sys
PATH = os.path.dirname(os.path.abspath(__file__))
if os.path.exists('%s/common'%PATH):
	sys.path.append('%s/common'%PATH)
else:
	sys.path.append('%s/../../../common'%PATH)

import os,os.path,sys,struct,time,traceback,signal,string,json

from gevent import monkey
monkey.patch_all()

from django.conf import settings


# if settings.datebase_is_pgsql()
# 	import psycogreen.gevent
# 	psycogreen.gevent.patch_psycopg()

import django
from bson.objectid import ObjectId


import init_script

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


import desert
from desert.base import  USER_ID,CALL_USER_ID
from desert.misc import currentTimestamp64
import nosql,cached
from koala.koala_impl import *
from koala.base import MessageConfirmValue


class MessagingServiceImpl(IMessageServer,IUserEventListener):
	def __init__(self,app):
		IMessageServer.__init__(self)
		#IUserTeamServer.__init__(self)
		IUserEventListener.__init__(self)
		self.app = app
		self.serviceprxlist={}  #服务器代理对象缓存
		self.usergws = {}


	def onUserOnline(self,userid,gws_id,device,ctx):
		print 'onUserOnline..',userid,gws_id
		# self.usergws[userid] = gws_id
		#保存用户状态到数据表
		# user = core.User.objects.get(id = int(userid))
		# user.status = UserStatus.Online
		# user.save()

		#传递未发送消息到前端用户
		self._sendPendingMsgToUser(userid)
		#self._sendPendingInvitationToInvitee(userid)
		#self._sendPendingInvitationActToInviter(userid)
		#self._sendPendingJoinTeamRequestToTeamOwner(userid)
		#self._sendPendingJoinTeamResultToRequester(userid)
		#self._sendNotifications(userid)
		#self._notifyUserStatusChanged(userid,UserStatus.Online)


	def onUserOffline(self,userid,gws_id,device,ctx):
		print 'onUserOffline.. \n do nothing..'
		# userid = int(userid)
		# gws = self.usergws.get(userid)
		# if gws != None:
		# 	del self.usergws[userid]
		# user = core.User.objects.get(id = int(userid))
		# user.status = UserStatus.Offline
		# user.save()
		# #通知所有用户告知本人离线
		# self._notifyUserStatusChanged(userid,UserStatus.Offline)

	# def confirmMessage(self, seqs, ctx):
	# 	IMessageServer.confirmMessage(self, seqs, ctx)
	#
	# def sendMessage(self, token_list, message, ctx):
	# 	IMessageServer.sendMessage(self, token_list, message, ctx)



	def _sendPendingMsgToUser(self,userid):
		'''
			发送未传送的消息到终端用户
		'''
		print '_sendPendingMsgToUser..',userid
		coll = nosql.get_collection(nosql.SendMessage)
		rs = coll.find({'target_id':userid,'confirm_result':0}) #.sort({})
		if not rs.count():
			return
		prx = self.getTerminalProxyByUserId(userid)
		if not prx:
			return
		print 'pending user message size:',rs.count()
		send_num = 0
		for r in rs:
			e = nosql.SendMessage().assign(r)
			self.sendMessage( e )


	def sendMessage(self,message):
		"""
		发送消息到终端客户
		:param
			message: (nosql.SendMessage)

		:return:
		"""
		prx = self.getTerminalProxyByUserId(message.target_id)
		target_id = message.target_id

		if message.is_simple():
			text = message.to_simple()
			prx.onSimpleText_oneway( text,CALL_USER_ID(target_id))
		else:
			msg = message.to_message()
			prx.onMessage_oneway( msg, CALL_USER_ID( target_id ))

	def confirmMessage(self,seq_id_list,ctx):
		"""
			seq_ids : list
			B 接收到消息之后发送 确认消息，
			否则系统将定时重发当初的消息或者当B再次在线online时被推送到B
		"""
		# print 'sendMessageConfirm..', 'seq_id:',seq_id
		user_id = USER_ID(ctx)
		try:
			coll = nosql.get_collection(nosql.SendMessage)
			for seq_id in seq_id_list:
				r = coll.find_one({'_id':ObjectId(seq_id),'target_id':user_id })
				m = nosql.SendMessage().assign(r)
				m.confirm_time = currentTimestamp64()
				m.confirm_result = MessageConfirmValue
				m.save()
		except:
			traceback.print_exc()


	def getTerminalProxyByUserId(self,user_id):
		'''
			server_eps.conf 记录gws对应的接收rpc消息的endpoint名称,
			获取ep名称，通过RpcCommunicator.findEndpoints()得到ep
			ep.impl就是对应服务器接收消息的连接
		'''
		prx = cached.getTerminalProxyByUserId(ServerAppMexs.instance().cache,user_id)
		return prx

#--------------- Server App -------------------------------------------

class ServerAppMexs( desert.app.BaseAppServer):
	def __init__(self,name='messageserver'):
		desert.app.BaseAppServer.__init__(self,name)

	def init(self):
		print 'server:(%s) initializing..'%self.name
		# print desert.app.BaseAppServer.init(self,'a','b')
		# print super(ServerAppMexs,self)
		# super(ServerAppMexs,self).init( init_script.GLOBAL_SETTINGS_FILE, init_script.GLOBAL_SERVICE_FILE)
		desert.app.BaseAppServer.init(self, init_script.GLOBAL_SETTINGS_FILE, init_script.GLOBAL_SERVICE_FILE)

		self.initLogs()
		nosql.database = self.mongo.db

		conn1 =self.getEndPointConnection('mq_messageserver')
		conn2 = self.getEndPointConnection('mq_user_event_listener')

		adapter  = tce.RpcAdapterMQ.create('server',conn1)
		adapter.addConnection(conn2)

		self.servant = MessagingServiceImpl(self)
		adapter.addServant(self.servant)
		print 'server initialized .'

	def initLogs(self):
		cfg = self.conf.get('log')
		if cfg:
			value = cfg.get('stdout')
			if value :
				self.getLogger().addHandler( desert.app.BaseAppServer.LOGCLS.StdoutHandler(sys.stdout))
			value = cfg.get('file')
			if value:
				self.getLogger().addHandler(desert.app.BaseAppServer.LOGCLS.FileHandler(value))
			value = cfg.get('dgram')
			if value:
				self.getLogger().addHandler(desert.app.BaseAppServer.LOGCLS.DatagramHandler(value))
		if self.getLogger().handlers:
			sys.stdout = self.getLogger()

	def run(self):
		self.init()

		super(ServerAppMexs,self).run(self)
		self.communicator.waitForShutdown()

	def sendMessage(self,app_id,token_list,message,simple=True):
		"""
			app_id :  应用标识
			token_list: 消息接收目标列表
			message:  消息内容 (Message_t)
			simple:  是否是简单消息内容
		"""
		for target_id in token_list:
			m = nosql.SendMessage().set_content(message,simple)
			m.target_id = target_id
			m.app_id = app_id
			m.save()
			self.servant.sendMessage( target_id,m)

	_handle = None
	@classmethod
	def instance(cls):
		if not cls._handle :
			cls._handle = cls()
		return cls._handle

if __name__ == '__main__':
	# ServerApp().run()
	nosql.test()