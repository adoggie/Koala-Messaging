#--coding:utf-8--


"""
	mexs - 消息交换服务器
		提供消息投递、转发、通知功能
	author: mark
	date:   2014.3.20
"""

import imp,os
PATH = os.path.dirname(os.path.abspath(__file__))
imp.load_source('init',PATH +'/../../init_script.py')

import gevent
from gevent import monkey
monkey.patch_all()
import psycogreen.gevent
psycogreen.gevent.patch_psycopg()


import lemon
from lemon import utils
from service.lemon_impl import *
# from service.server import ServerApp
from  lemon.utils.app import BaseAppServer
import  model.django.core.models as  core
# from bson.objectid import ObjectId

class MessagingServiceImpl(IMessageServer,IUserEventListener):
	def __init__(self,app):
		IMessageServer.__init__(self)
		IUserEventListener.__init__(self)
		self.app = app

	def sendNotification(self, target_unit, target_user_role, msg, ctx):
		IMessageServer.sendNotification(self, target_unit, target_user_role, msg, ctx)
		redis = BaseAppServer.instance().cache
		key = lemon.basetype.CacheEntryFormat.UnitRelatedUsers%target_unit
		redis.get( key )
		# users = core.OrgUser.objects.filter(unit__id=int(target_unit))\
		# 	.extra(where=[core.OrgUser.getClauseWhere_Role(int(target_user_role))])
		users = []
		unit = core.OrgUnit.objects.get(id = int(target_unit))
		temp ={}
		if target_user_role & core.OrgUser.ROLE_RECIEVER:
			users += unit.recv_user_set.all()
		if target_user_role & core.OrgUser.ROLE_SENDER:
			users += unit.send_user_set.all()
		for user in users:
			temp[user.id] = user

		for k,user in temp.items():
			userid = user.id
			prx = self._getTerminalProxyByUserId(userid)
			if not prx:
				continue
			prx.onNotifyMessage_oneway(msg,lemon.base.CALL_USER_ID(userid))


	def onUserOnline(self,userid,gws_id,device,ctx):
		print 'onUserOnline..',userid,gws_id



	def onUserOffline(self,userid,gws_id,device,ctx):
		print 'onUserOffline..'



	def _getTerminalProxyByUserId(self,user_id):
		"""
			server_eps.conf 记录gws对应的接收rpc消息的endpoint名称,
			获取ep名称，通过RpcCommunicator.findEndpoints()得到ep
			ep.impl就是对应服务器接收消息的连接
		"""
		prx = lemon.cached.getTerminalProxyByUserId(BaseAppServer.instance().cache,user_id)
		return prx

#--------------- Server App -------------------------------------------

class ServerApp(utils.app.BaseAppServer):
	def __init__(self,name):
		utils.app.BaseAppServer.__init__(self,name)

	def initNosql(self):
		pass

	def run(self):
		import service.config

		self.init(service.config.GLOBAL_SETTINGS_FILE,service.config.GLOBAL_SERVICE_FILE)
		# lemon.nosql.database = self.mongo.db

		server =self.getEndPointConnection('mq_messageserver')
		conn = self.getEndPointConnection('mq_user_event_listener')
		adapter  = tce.RpcAdapterMQ.create('server',server)
		adapter.addConnection(conn)

		servant = MessagingServiceImpl(self)
		adapter.addServant(servant)

		utils.app.BaseAppServer.run(self)
		self.communicator.waitForShutdown()


if __name__ == '__main__':
	ServerApp('mexs').run()
