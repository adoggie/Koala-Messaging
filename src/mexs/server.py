#--coding:utf-8--


'''
	mexs - 消息交换服务器
		提供消息投递、转发、通知功能
	author: mark
	date:   2014.3.20

	目前仅考虑单点设备登录
'''

import os
PATH = os.path.dirname(os.path.abspath(__file__))
if os.path.exists('%s/common'%PATH):
	sys.path.append('%s/common'%PATH)
else:
	sys.path.append('%s/../common'%PATH)

import os,os.path,sys,struct,time,traceback,signal,string,json

from gevent import monkey
monkey.patch_all()
import psycogreen.gevent
psycogreen.gevent.patch_psycopg()


from django.db import transaction
from bson.objectid import ObjectId


import init_script

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


import desert
from desert.base import  USER_ID,CALL_USER_ID

import  model.core.models as  core
import nosql,cached
from koala.koala_impl import *


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
		userid = int(userid)
		self.usergws[userid] = gws_id
		#保存用户状态到数据表
		user = core.User.objects.get(id = int(userid))
		user.status = UserStatus.Online
		user.save()
		#传递未发送消息到前端用户
		self._sendPendingMsgToUser(userid)
		# self._sendPendingInvitationToInvitee(userid)
		#self._sendPendingInvitationActToInviter(userid)
		#self._sendPendingJoinTeamRequestToTeamOwner(userid)
		#self._sendPendingJoinTeamResultToRequester(userid)
		self._sendNotifications(userid)
		self._notifyUserStatusChanged(userid,UserStatus.Online)


	def onUserOffline(self,userid,gws_id,device,ctx):
		print 'onUserOffline..'
		userid = int(userid)
		gws = self.usergws.get(userid)
		if gws != None:
			del self.usergws[userid]
		user = core.User.objects.get(id = int(userid))
		user.status = UserStatus.Offline
		user.save()
		#通知所有用户告知本人离线
		self._notifyUserStatusChanged(userid,UserStatus.Offline)

	def confirmMessage(self, seqs, ctx):
		IMessageServer.confirmMessage(self, seqs, ctx)

	def sendMessage(self, token_list, message, ctx):
		IMessageServer.sendMessage(self, token_list, message, ctx)

	#------------- IUserTeamServer --------------------------------------

	def sendTeamMessageText(self,team_id,text,ctx):
		'''
			发送消息到指定的群
		'''

		print 'sendTeamMessageText..',team_id

		userid = USER_ID1(ctx)
		#群内非本人所有朋友记录, 群主不在 teamrelation表哦,
		users=[]
		team_id = team_id
		team = None
		cr = ErrorDefs.SUCC
		try:
			team = core.UserTeam.objects.get(id=team_id)
		except:
			#return ErrorDefs.TargetObjectNotExisted #发送对象不存在，发送端删除发送记录，取消再次发送
			return
		if team.user.id != userid: #不是本人的team,把team的owner也加入群发数组
			users.append(team.user)

		rs = core.TeamRelation.objects.filter(team__id=int(team_id)).exclude(user__id=userid)
		for r in rs:
			use

	def nofityConfirm(self,seq_id,ctx):
		'''
			除了消息发送、邀请之外的处理类型，需要确认接收到了，必须走此接口
		'''
		userid = USER_ID(ctx) #当前用户编号
		coll = nosql.get_collection(nosql.Notification)
		r = coll.find_one({'_id':ObjectId(seq_id),'target_id':userid})
		e = nosql.Notification().assign(r)
		e.confirm_time = sns.utils.misc.currentTimestamp64()
		e.save()

	def _sendNotifications(self,userid):
		prx = self.__getTerminalProxyByUserId(userid)
		if not prx:
			return
		#提取未发送的通知消息
		coll = nosql.get_collection(nosql.Notification)
		rs = coll.find({'target_id':userid,'confirm_time':None}) #.sort({'issue_time':1})


		# ents = nosql.Notification.objects.filter(target_id=int(userid),confirm_time=None).order_by('issue_time')
		for r in rs:
			nm = nosql.Notification().assign(r).toMessage()
			# print nm.type_,nm.seq
			prx.onNotifyMessage_oneway( nm.issuer,nm,CALL_USER_ID(userid))


	def _sendPendingMsgToUser(self,userid):
		'''
			发送未传送的消息到终端用户
		'''
		print '_sendPendingMsgToUser..',userid
		# ents = nosql.SendMessage.objects.filter(target_id=userid,confirm_result=SendMsgStatus.UNACKED).order_by('issue_time')
		coll = nosql.get_collection(nosql.SendMessage)
		rs = coll.find({'target_id':userid,'confirm_result':SendMsgStatus.UNACKED}) #.sort({})
		if not rs.count():
			return
		prx = self.__getTerminalProxyByUserId(userid)
		if not prx:
			return
		print 'pending user message size:',rs.count()
		send_num = 0
		for r in rs:
			e = nosql.SendMessage().assign(r)
			m = MimeText_t()
			m.seq =  e.id()
			m.text = e.content
			m.issue_time = e.issue_time
			m.type = e.type
			m.entities = e.entities
			print e.issue_time,str(e.issue_time),type(e.issue_time)
			if not e.team_id: # not null or  not 0
				prx.onMessageText_oneway(str(e.sender_id),m,CALL_USER_ID(userid))
				send_num+=1
				print 'send num:',send_num,'seq:',m.seq
			else: #传递到用户组
				prx.onTeamMessageText_oneway(str(e.sender_id),e.team_id,m,CALL_USER_ID(userid))


	def sendMessageText(self,target_id,text,ctx):
		print 'sendMessageText:', target_id,text.issue_time,text.text
		userid = USER_ID(ctx)
		text.issue_time = sns.utils.misc.currentTimestamp64()

		m = nosql.SendMessage()
		#m.sid = utils.misc.genUUID()
		m.sender_id = userid
		m.target_id = int(target_id)
		# m.team_id = 0
		# m.type = text.type_
		m.type = MsgTargetType.USER
		m.level = SendMsgLevel.DURABLE
		m.content = text.text  #to see MineText_t
		m.entities = text.entities
		m.userdata = text.userdata
		m.save()
		# self._ripMessageContent(m,text)
		m.datas=[]
		text.seq = m.id()
		#查询目标用户是否接入到某个gws,并将消息传送过去
		prx = self.__getTerminalProxyByUserId(target_id)
		print 'prx is:',prx
		if prx :
			prx.onMessageText_oneway(str(userid),text,CALL_USER_ID(target_id))
		#return ErrorDefs.SUCC





	def sendMessageConfirm(self,seq_id,ctx):
		'''
			B 接收到消息之后发送 确认消息，
			否则系统将定时重发当初的消息或者当B再次在线online时被推送到B
		'''
		print 'sendMessageConfirm..', 'seq_id:',seq_id
		userid = USER_ID(ctx)
		try:
			coll = nosql.get_collection(nosql.SendMessage)
			# m = nosql.SendMessage.objects.get(id=int(seq_id),target_id=int(userid))
			r = coll.find_one({'_id':ObjectId(seq_id),'target_id':int(userid)})
			m = nosql.SendMessage().assign(r)
			#m.issue_time = utils.misc.currentTimestamp64() # sqlite 时，m.issue_time 会莫名其妙的为null, issue_time必须设置为null=True即可通过
			m.confirm_time = sns.utils.misc.currentTimestamp64()
			m.confirm_result = SendMsgStatus.ACKED
			m.save()
			#发送通知到消息发送者
			nfc = nosql.Notification(sender_id=userid,
						target_id=m.sender_id,
						type=NotifyMsgType.PeerMessageReceived)
			nfc.p1 = m.userdata
			nfc.save()

			prx = self.__getTerminalProxyByUserId(m.sender_id)
			if  prx:
				nm =  nfc.toMessage()
				prx.onNotifyMessage_oneway( nm.issuer,nm,CALL_USER_ID(m.sender_id))
		except:
			traceback.print_exc()




	def __getTerminalProxyByUserId(self,user_id):
		'''
			server_eps.conf 记录gws对应的接收rpc消息的endpoint名称,
			获取ep名称，通过RpcCommunicator.findEndpoints()得到ep
			ep.impl就是对应服务器接收消息的连接
		'''
		prx = cached.getTerminalProxyByUserId(ServerApp.instance().cache,user_id)
		return prx

#--------------- Server App -------------------------------------------

class ServerApp( desert.app.BaseAppServer):
	def __init__(self,name):
		desert.app.BaseAppServer.__init__(self,name)
		# self.prxlocserver = None

	def getLocationServerProxy(self):
		return self.prxlocserver

	def run(self):
		self.init( init_script.GLOBAL_SETTINGS_FILE, init_script.GLOBAL_SERVICE_FILE)
		nosql.database = self.mongo.db

		# conn = self.getEndPointConnection('mq_locationserver')
		# self.prxlocserver = ILocationServerPrx(conn)

		server =self.getEndPointConnection('mq_messageserver')
		conn = self.getEndPointConnection('mq_user_event_listener')
		adapter  = tce.RpcAdapterMQ.create('server',server)
		adapter.addConnection(conn)

		servant = MessagingServiceImpl(self)
		adapter.addServant(servant)

		super(ServerApp,self).run(self)
		# sns.utils.app.BaseAppServer.run(self)
		self.communicator.waitForShutdown()


if __name__ == '__main__':
	ServerApp('messageserver').run()
