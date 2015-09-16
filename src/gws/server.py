#--coding:utf-8--

"""
2014.6.26 scott
	1.增加注册到redirector功能


"""

import imp,os
PATH = os.path.dirname(os.path.abspath(__file__))
if os.path.exists('%s/../common'%PATH):
	sys.path.append('%s/../common'%PATH)
else:
	sys.path.append('%s/../../common'%PATH)


import init_script

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import os,os.path,sys,struct,time,traceback,signal,string

import gevent
from gevent import monkey
monkey.patch_all()
import psycogreen.gevent
psycogreen.gevent.patch_psycopg()


import tcelib as tce
import koala
import uuid,copy
import settings
import desert



HEARTBEAT_TIMEOUT = 20*1000 # 20s之内必须接收到一个心跳
# USERTOKEN_EXPIRE_TIME = 3600 * 5 # 5 天

class EventListener(tce.RpcConnectionEventListener):
	def __init__(self,server):
		tce.RpcConnectionEventListener.__init__(self)
		self.server = server


	def isTokenSessionExpired(self,auth):
		"""
			是否token会话信息过期
		"""
		return False
		if time.time() > auth.expire_time:
			return True
		return False

	def connectReject(self,error,conn):
		"""
			发送通知到前端设备
		"""
		try:
			termPrx = koala.ITerminalPrx(conn)
			nm = NotifyMessage_t(type_=lemon.base.NotifyMsgType.ConnectTgsReject,
					p1=error,
					issue_time= utils.misc.currentTimestamp64()
					)
			termPrx.onNotifyMessage_oneway(nm)
			conn.close()
		except:
			traceback.print_exc()

	def onDataPacket(self, conn, m):
		'''
			接收到第一个消息包进行检测
				1.检查token是否合法
				2.检查device_id与token是否是同一台设备发出
				3.如果不一致，返回错误信息，通过ITermnial.onNotifyMessage()传递到前端设备
			@return:
				False - tce将关闭connection
				True - okay
		'''
		if conn.getRecvedMessageCount() == 1:
			error = desert.base.ErrorDefs.SUCC

			token = m.extra.getValue('__token__')
			if token:
				auth = desert.auth.decryptUserToken(token)
				if auth:
					if self.isTokenSessionExpired(auth):
						error = desert.base.ErrorDefs.UserTokenSessionExpired
					else:
						userid = auth.user_id
						conn.setUserId(int(userid))
						self.server.onUserOnline(userid,'',conn)
						print 'user check passed, user:',auth.user_id,auth.user_name
				else:
					error = desert.base.ErrorDefs.UserTokenInvalid
			else:
				error = desert.base.ErrorDefs.UserTokenInvalid

			if error:
				self.connectReject(error,conn)
				conn.recvpkg_num= 0
				# conn.close()
				return False

		if conn.appuser:
			conn.appuser.update()	#更新用户状态

		return True

	def onDisconnected(self, conn):
		tce.RpcConnectionEventListener.onDisconnected(self, conn)
		print 'onDisconnected..'
		userid = conn.getUserId()
		if userid:
			self.server.onUserOffline(userid,conn)

	def onConnected(self, conn):
		#tce.RpcConnectionEventListener.onConnected(self, conn)
		print 'onConnected..'

class TerminalUser:
	"""
		终端用户
	"""

	def __init__(self,userid,conn):
		self.userid = userid
		self.livetime = int(time.time())
		self.conn = conn

	def update(self):
		self.livetime = int(time.time())



class TerminalGatewayServer(koala.ITerminalGatewayServer):
	def __init__(self):
		koala.ITerminalGatewayServer.__init__(self)
		self.users={}   # {userid:heartbeat_time}

		gevent.spawn(self._threadTerminalLifeCheck)

		self.prxUserEventListener = koala.IUserEventListenerPrx.createWithEpName('mq_user_event_listener')
		self.listener = EventListener(self)
		tce.RpcCommunicator.instance().setConnectionEventListener(self.listener)

		self.redis = ServerApp.instance().cache

		self.redirector_ep = ''


	def onUserOnline(self,userid,device_id,conn):
		serverid = tce.RpcCommunicator.instance().currentServer().getName()   #server_eps.conf 对应 server_id 与 mq 名称
		self.prxUserEventListener.onUserOnline_oneway(str(userid),str(serverid),0)
		user = TerminalUser(userid,conn)
		self.users[userid] = user
		conn.appuser = user #可以使用conn.delta 替代
		self.redis.set(lemon.basetype.CacheEntryFormat.UserWithTGS%userid,serverid,HEARTBEAT_TIMEOUT)
		# self.redis.set(lemon.basetype.CacheEntryFormat.UserWithDevice%userid,device_id,HEARTBEAT_TIMEOUT)


	def onUserOffline(self,userid,conn):
		serverid = tce.RpcCommunicator.instance().currentServer().getName()
		self.prxUserEventListener.onUserOffline_oneway(str(userid),str(serverid),0)
		if self.users.has_key(userid):
			del self.users[userid]

		#缓存redis 记录用户由哪个tgs接入
		serverid = tce.RpcCommunicator.instance().currentServer().getName()
		self.redis.delete(lemon.basetype.CacheEntryFormat.UserWithTGS%userid)
		# self.redis.delete(lemon.basetype.CacheEntryFormat.UserWithDevice%userid)

	def onUserLogin(self, user_id, login_tgs, targetTgs, ctx):
		'''
		其他tgs发送通知用户登录，要求本地已接入的user退出登录
		'''
		if ServerApp.instance().name != targetTgs:	#不是本人的消息
			return
		#找到指定user_id的连接 conn ,发送下线通知
		adapter = ServerApp.instance().getSocketAdatper()
		conn = adapter.getUserConnection( int(user_id) )
		if conn:
			self.listener.connectReject(lemon.base.ErrorDefs.UserAnotherPlaceLogin,conn)
			conn.recvpkg_num= 0


	def ping(self, ctx):
		ITerminalGatewayServer.ping(self, ctx)
		print lemon.utils.misc.currentDateTimeStr(), 'ping() from: ',ctx.conn.getAddress()
		userid = ctx.conn.getUserId()

		serverid = tce.RpcCommunicator.instance().currentServer().getName()   #server_eps.conf 对应 server_id 与 mq 名称
		self.redis.set(lemon.basetype.CacheEntryFormat.UserWithTGS%userid,serverid,HEARTBEAT_TIMEOUT)

	def _threadTerminalLifeCheck(self):
		'''
			定时检查每个连接最新活动时间，超时则释放连接资源
		'''

		while True:
			gevent.sleep(5)
#			print 'check user connection..'
			invalid_users = []
			for userid,user in self.users.iteritems():
				if int(time.time()) - user.livetime > HEARTBEAT_TIMEOUT:
					invalid_users.append( user )
			for user in invalid_users:
				user.conn.close()

#
def usage():
	print ' pygwa.py -type [gwa|direct] -name gwa1 -config services.xml -eps gwa1_socket,..'
	print 'examples:'
	print 'pygwa.py -name gwa_1 -config ./services.xml -listen gwa1_socket,mq_gateway1 -loopback mq_messageserver#mq_gateway1,mq_userserver#mq_gateway1'


class ServerApp(desert.app.BaseAppServer):
	def __init__(self,name):
		desert.app.BaseAppServer.__init__(self,name)

	def initNosql(self):
		pass


	def initDatabase(self):
		cfg = self.yamlcfg[self.conf.get('postgresql')]
		if cfg:
			dbname = cfg['dbname']
			host = cfg['host']
			port = cfg['port']
			user = cfg['user']
			passwd = cfg['passwd']
			settings.DATABASES['default']['NAME'] = dbname
			settings.DATABASES['default']['USER'] = user
			settings.DATABASES['default']['PASSWORD'] = passwd
			settings.DATABASES['default']['HOST'] = host
			settings.DATABASES['default']['PORT'] = port


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

	def getSocketAdapter(self):
		adapter = None
		eps = tce.RpcCommunicator.instance().currentServer().name_eps.values()
		for ep in eps:
			if ep.type in ('socket','websocket'):
				adapter = ep.impl
				break
		return adapter

	def run(self):
		self.init(init_script.GLOBAL_SETTINGS_FILE,init_script.GLOBAL_SERVICE_FILE)
		# lemon.nosql.database = self.mongo.db
		self.initLogs()
		self.initDatabase()

		desert.app.BaseAppServer.run(self)
		# self.communicator.waitForShutdown()

def main():
	argv = copy.deepcopy(sys.argv)
	name = ''
	cfg =''
	eps_listen=[]
	loopbacks=[]
	type='gwa' # or direct

	try:
		while argv:
			p = argv.pop(0).strip().lower()

			if p =='-name':
				name = argv.pop(0)
			if p=='-config':
				cfg = argv.pop(0)
			if p == '-listen':
				eps_listen = argv.pop(0)
				eps_listen = eps_listen.split(',')
			if p == '-loopback':
				s = argv.pop(0)
				pairs = s.split(',')
				for p in pairs:
					call,return_ = p.split('#')
					loopbacks.append( (call,return_) )
			if p == '-redirector':
				redirector = argv.pop(0)
	except:
		usage()
		return

	if  not eps_listen:
		usage()
		return

	ServerApp(name).run()
	servant = TerminalGatewayServer()

	for ep in eps_listen:
		ep = ep.strip()
		id = uuid.uuid4().hex
		adapter = tce.RpcCommunicator.instance().createAdapter(id,ep)
		adapter.addServant(servant)

	for lpb in loopbacks:
		lpb = map(string.strip,lpb)
		call,back = lpb
		ep1 = tce.RpcCommunicator.instance().currentServer().findEndPointByName(call)
		ep2 = tce.RpcCommunicator.instance().currentServer().findEndPointByName(back)
		if not ep1 or not ep2:
			print 'error: loopback items <%s> not found!'%str(lpb)
			return -1
		if ep1.type not in ('mq','qpid')  or ep2.type not in ('mq','qpid'):
			print 'error: loopback items <%s> must be mq type!'%str(lpb)
			return -1
		ep1.impl.setLoopbackMQ(ep2.impl)

#	print name,cfg,eps,type
	print 'Instance:',name,' started \nwaiting for shutdown..'
	tce.RpcCommunicator.instance().waitForShutdown()

if __name__ == '__main__':
	# if sys.argv[-1] =='websocket':
	p ='gwserver.py -name gwserver -listen websocket_gateway_1,mq_gateway_1,mq_gateway_broadcast -loopback mq_messageserver#mq_gateway_1'
	print 'start <<WEBSOCKET>>..'

	sys.argv = p.split(' ')
	sys.exit( main())
