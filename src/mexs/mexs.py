#coding:utf-8


"""
    mexs - 消息交换服务器
        提供消息投递、转发、通知功能
    author: mark
    date:   2014.3.20

    目前仅考虑单点设备登录

pymongo
  http://api.mongodb.com/python/current/tutorial.html


"""

import time
import os.path
import traceback

import pymongo
from bson.objectid import ObjectId
from camel.biz.application.camelsrv import instance
from camel.koala.koala import IMessageServer,IUserEventListener,Message_t,MessageMeta_t,Properties_t
from camel.koala.base import CALL_USER_ID,USER_ID
import nosql
import cached


class MessagingServiceImpl(IMessageServer,IUserEventListener):
    def __init__(self,server):
        IMessageServer.__init__(self)
        IUserEventListener.__init__(self)
        self.server = server
        self.serviceprxlist={}  #服务器代理对象缓存
        self.usergws = {}


    def onUserOnline(self,userid,gws_id,device,ctx):
        instance.getLogger().debug('onUserOnline: {},{}'.format(userid,gws_id) )
        #传递未发送消息到前端用户
        self.sendPendingMsgToUser(userid)


    def onUserOffline(self,userid,gws_id,device,ctx):
        instance.getLogger().debug('onUserOffline: {},{}'.format(userid, gws_id))

    def sendMessage(self, targets, message, ctx):
        """
        向目标对象传递消息
        消息进入缓存,用户在线则即刻传递

        :param targets: list(string)
        :param message: Message_t
        :param ctx:
        :return:
        """
        user_id = USER_ID(ctx)
        if not user_id:
            user_id = message.meta.sender
        db = self.server.getMongoDatabaseConnection().db
        for target_id in targets:
            name = nosql.KoalaCollection.getUserMessageCollection(target_id)
            coll = db[name]

            # r = user_msg_col.find_one( {'_id':ObjectId(sid) })
            data = {
                'realm': message.meta.realm,
                'sender_id': user_id,
                'send_time': int(time.time())*1000,
                'title': message.title,
                'content':message.content,
                'props': message.props,
                nosql.UserMessageStatus.FIELD: nosql.UserMessageStatus.Sendable
            }
            _id = coll.insert( data )
            message.meta.seq = str(_id)
            prx = self.getTerminalProxyByUserId(target_id)  # 搜寻一个匹配的接入服务器的代理对象
            if not prx:
                instance.getLogger().warn("user server(mgws) not found: {} ".format(target_id))
                continue
            prx.onMessage_oneway(message, CALL_USER_ID(target_id))
            instance.getLogger().debug("message be delivered to destination: from:{} to:{} ".format(user_id,target_id))

    def sendPendingMsgToUser(self,user_id):
        """
            发送未传送的消息到终端用户
        """
        instance.getLogger().debug('_sendPendingMsgToUser: {}'.format(user_id))
        db = self.server.getMongoDatabaseConnection().db
        name = nosql.KoalaCollection.getUserMessageCollection(user_id)

        user_msg_col = db[ name ]

        # 检索用户可待发送的消息列表
        # sort("UserName", pymongo.ASCENDING)

        rs = user_msg_col.find({ nosql.UserMessageStatus.FIELD:nosql.UserMessageStatus.Sendable}).sort("send_time", pymongo.DESCENDING)

        if rs.count() == 0:
            instance.getLogger().debug('message collection is null !')
            return

        prx = self.getTerminalProxyByUserId(user_id) # 搜寻一个匹配的接入服务器的代理对象
        if not prx:
            instance.getLogger().warn("user server(mgws) not found: {} ".format(user_id))
            return
        instance.getLogger().debug("user message: {} will be dispatched.".format(rs.count()))

        for row  in rs:
            m = Message_t()
            m.meta.realm = row.get('realm','')
            m.meta.seq = row.get('_id')
            m.meta.sender = row.get('sender_id')
            m.meta.stime = row.get('send_time')
            m.title = row.get('title','')
            m.content = row.get('content','')
            m.props = row.get('props',{})
            prx.onMessage_oneway(m,CALL_USER_ID(user_id))


    def acknowledge(self,sids,ctx):
        """
            seq_ids : list
            B 接收到消息之后发送 确认消息，
            否则系统将定时重发当初的消息或者当B再次在线online时被推送到B
        """
        user_id = USER_ID(ctx)
        db = self.server.getMongoDatabaseConnection().db
        name = nosql.KoalaCollection.getUserMessageCollection(user_id)
        coll = db[name]
        print sids
        for sid in sids:
            coll.update({'_id':ObjectId(sid) },
                        {'$set': {
                            nosql.UserMessageStatus.FIELD:nosql.UserMessageStatus.Confirmed,
                            'confirm_time':int(time.time())
                            } }
                        )
            instance.getLogger().debug('message sid acked :{}'.format(sid))


    def getTerminalProxyByUserId(self,user_id):
        """
            server_eps.conf 记录gws对应的接收rpc消息的endpoint名称,
            获取ep名称，通过RpcCommunicator.findEndpoints()得到ep
            ep.impl就是对应服务器接收消息的连接
        """
        cache = instance.getCache()
        prx = cached.getTerminalProxyByUserId(cache,user_id)
        return prx


"""
db.Account.remove()   -- 全部删除
db.Account.insert({"AccountID":21,"UserName":"libing"})
db.Account.update({"UserName":"libing"},{"$set":{"Email":"libing@126.com","Password":"123"}})
db.Account.find().sort([("UserName",pymongo.ASCENDING),("Email",pymongo.DESCENDING)])

"""
