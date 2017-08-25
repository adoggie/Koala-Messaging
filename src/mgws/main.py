#coding:utf-8


import sys
import time
import traceback
import string
import uuid
import copy

import gevent

if False:
    import psycogreen.gevent
    psycogreen.gevent.patch_psycopg()

from camel.biz.application.camelsrv import instance
from camel.koala import tcelib as tce
from camel.koala.koala import ITerminalGatewayServer,IUserEventListenerPrx,ITerminalPrx,Message_t
from camel.koala import base,errors
from camel.koala.base import CacheEntryConfig
from camel.koala.errors import ErrorDefs
# from camel.koala.token import  decode_user_token
# from camel.fundamental.utils.useful import ObjectBuilder
from connection import EventListener

HEARTBEAT_TIMEOUT_DEFAULT = 300
USERTOKEN_EXPIRE_TIME_DEFAULT = 3600 * 12 * 5


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


class TerminalGatewayServerImpl(ITerminalGatewayServer):
    def __init__(self,server):
        ITerminalGatewayServer.__init__(self)
        self.users={}   # {userid:heartbeat_time}
        self.server = server
        gevent.spawn(self._threadTerminalLifeCheck)

        self.prxUserEventListener = IUserEventListenerPrx.createWithEpName('mq_user_event_listener')
        self.listener = EventListener(self)
        tce.RpcCommunicator.instance().setConnectionEventListener(self.listener)

        self.redis = instance.getCache()
        self.redirector_ep = ''

    def onUserOnline(self,userid,device_id,conn):
        """
        用户连接上线触发
        :param userid:
        :param device_id:
        :param conn:
        :return:
        """
        serverid = tce.RpcCommunicator.instance().currentServer().getName()   			#server_eps.conf 对应 server_id 与 mq 名称
        self.prxUserEventListener.onUserOnline_oneway(str(userid),str(serverid),0)  # 传递用户上线通知到 mexs 服务
        user = TerminalUser(userid,conn)
        self.users[userid] = user

        conn.appuser = user             #可以使用conn.delta 替代
        self.redis.set( CacheEntryConfig.getUserKey(userid),serverid,
                        instance.getConfig().get('access_heartbeat_timeout',HEARTBEAT_TIMEOUT_DEFAULT))

    def onUserOffline(self,userid,conn):
        serverid = tce.RpcCommunicator.instance().currentServer().getName()
        self.prxUserEventListener.onUserOffline_oneway(str(userid),str(serverid),0)
        if self.users.has_key(userid):
            del self.users[userid]

        #缓存redis 记录用户由哪个tgs接入
        # serverid = tce.RpcCommunicator.instance().currentServer().getName()
        if True:
            self.redis.delete( CacheEntryConfig.getUserKey(userid) )

        # self.redis.delete(lemon.basetype.CacheEntryFormat.UserWithDevice%userid)

    def onUserLogin(self, user_id, login_tgs, targetTgs, ctx):
        """
            其他tgs发送通知用户登录，要求本地已接入的user退出登录
        """
        if instance.name != targetTgs:	#不是本人的消息
            return
        #找到指定user_id的连接 conn ,发送下线通知
        adapter = self.getSocketAdatper()
        conn = adapter.getUserConnection( user_id ) # 找到接入指定用户的连接对象
        if conn:
            self.listener.connectReject(ErrorDefs.UserAnotherPlaceLogin,conn) # 发送断开通知消息
            conn.recvpkg_num= 0

    def getSocketAdapter(self):
        adapter = None
        eps = tce.RpcCommunicator.instance().currentServer().name_eps.values() # 返回所有的通信端点
        for ep in eps:
            if ep.type in ('socket', 'websocket'):
                adapter = ep.impl
                break
        return adapter

    def ping(self, ctx):
        ITerminalGatewayServer.ping(self, ctx)
        user_id = ctx.conn.getUserId()
        instance.getLogger().debug("user ping.. {} {}".format( user_id,ctx.conn.getAddress()))

        # print desert.misc.currentDateTimeStr(), 'ping() from: ',ctx.conn.getAddress()

        serverid = tce.RpcCommunicator.instance().currentServer().getName()                 # against to server_eps.conf 对应 server_id 与 mq 名称
        self.redis.set( CacheEntryConfig.getUserKey( user_id ),serverid,
                        instance.getConfig().get('access_heartbeat_timeout', HEARTBEAT_TIMEOUT_DEFAULT))

    def _threadTerminalLifeCheck(self):
        """
            定时检查每个连接最新活动时间，超时则释放连接资源
        """
        while True:
            gevent.sleep(5)
            invalid_users = []
            for userid,user in self.users.iteritems():
                if int(time.time()) - user.livetime > instance.getConfig().get('access_heartbeat_timeout',HEARTBEAT_TIMEOUT_DEFAULT) :
                    invalid_users.append( user )
            for user in invalid_users:
                user.conn.close()


__all__=(TerminalGatewayServerImpl,)