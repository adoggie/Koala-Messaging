#coding:utf-8

import traceback
import os.path

from camel.fundamental.parser.kvpair import SimpleConfig
from camel.biz.application.camelsrv import instance
from camel.koala.base import CacheEntryConfig
from camel.koala import tcelib as tce
from camel.koala.koala import ITerminalPrx

mgws_proxies ={}

def getTerminalProxyByUserId(cache,user_id):
    """根据终端用户id查找在连接到哪个tgs服务器
        server_eps.conf 记录tqs对应的接收rpc消息的endpoint名称,
        获取ep名称，通过RpcCommunicator.findEndpoints()得到ep
        ep.impl就是对应服务器接收消息的连接
    """
    global mgws_proxies
    prx = None
    try:
        key =  CacheEntryConfig.getUserKey(user_id)
        instance.getLogger().debug( 'cache.get: {}'.format(key) )
        mgws = cache.get(key) # return mgws-server's name
        if  not mgws:
            return None

        prx = mgws_proxies.get(mgws)
        if not prx:
            cf = SimpleConfig()
            eps_path = os.path.join(instance.getConfigPath(), 'server_eps.conf')
            cf.load(eps_path)
            ep_name = cf.getValue(mgws)
            conn = tce.RpcCommunicator.instance().getConnectionMQCollection().get(ep_name)
            if conn:
                prx = ITerminalPrx( conn )
                mgws_proxies[mgws] = prx
    except:
        traceback.print_exc()

    finally:
        if not prx:
            instance.getLogger().info('user: {} is offline.'.format(user_id))
        return prx


