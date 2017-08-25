#coding:utf-8


import time
from flask import Blueprint,request,g
from camel.fundamental.application.app import instance

from .decorator import user_access_token_check
from camel.koala.koala import Message_t
from camel.koala.webapi import CallReturn,ErrorDefs,ErrorReturn

@user_access_token_check
def message_send():
    """ 发送消息

    :return:
    """
    realm = request.values.get('realm','')
    users = request.values.get('users','')
    title = request.values.get('title','')
    content = request.values.get('content','')
    expire = request.values.get('expire',0)   # 消息有效时间 0: 永远有效
    execute = request.values.get('execute',0) # 预定推送时间 0:即刻执行

    prx = instance.getMessageServerProxy()

    sids = users.split(',')
    msg = Message_t()
    msg.meta.realm = realm
    msg.meta.sender = g.user.user_id
    msg.meta.stime = int(time.time())
    msg.title = title
    msg.content = content
    prx.sendMessage_oneway(sids,msg,extra=dict(expire= str(expire),execute= str(execute) ))
    return CallReturn().response


@user_access_token_check
def message_ack():
    """ 确认消息

    :return:
    """
    sids = request.values.get('sids', '')
    sids = sids.split(',')
    sids = filter(lambda _:_,sids)
    if sids:
        prx = instance.getMessageServerProxy()
        prx.acknowledge_oneway(sids,extra={'__user_id__':g.user.user_id})
    return CallReturn().response


@user_access_token_check
def message_query():
    """
    根据 (koala.idl) Message_t::Properties_t 查询满足条件的消息
    输出默认按时间降序输出 (最近24小时)
    :return:
    """
    props = request.values.get('props','')
    stime = request.values.get('start',int(time.time()) -  3600*24 )  # 默认近一天的消息
    etime = request.values.get('end',int(time.time()))
    limit = request.values.get('limit',100)
    text = request.values.get('text','') # 指定的过滤文本

    # 直接查询数据库
    db = instance.getMongoDatabaseConnection().db
    # db.message