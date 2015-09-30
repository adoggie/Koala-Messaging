#--coding:utf-8--

import os,traceback

import tcelib as tce
import desert
from koala import base
from koala.koala_impl import ITerminalPrx
import init_script

etc_path = init_script.ETC_PATH + '/server_eps.conf'
tgs_proxies ={}

def getTerminalProxyByUserId(cache,user_id):
	"""根据终端用户id查找在连接到哪个tgs服务器
		server_eps.conf 记录tqs对应的接收rpc消息的endpoint名称,
		获取ep名称，通过RpcCommunicator.findEndpoints()得到ep
		ep.impl就是对应服务器接收消息的连接
	"""
	global tgs_proxies
	prx = None
	try:
		key =  base.CacheEntryFormat.UserWithTGS%user_id
		print 'cache.get:',key
		tgs = cache.get(key)
		if  not tgs:
			print 'user %s is offline.'
			return None #not online
		# print key ,tgs_proxies
		prx = tgs_proxies.get(tgs)
		if not prx:
			cf = desert.config.SimpleConfig()
			cf.load(etc_path)
			epname = cf.getValue(tgs)
			ep = tce.RpcCommunicator.instance().currentServer().findEndPointByName(epname)
			prx = ITerminalPrx(ep.impl)
			tgs_proxies[tgs] = prx
	except:
		traceback.print_exc()
	finally:
		if not prx:
			print 'user: %s is not online!'%user_id
		return prx

# def cacheUserIdToTGS(cache,tgs_id,user_id):
# 	'''
# 		缓存用户由哪个tgs接入
# 		@param:
# 			tgs_id -
# 			user_id
# 	'''
# 	try:
# 		key = base.CacheEntryFormat.UserWithTGS(user_id)
# 		cache.set(key,tgs_id)
# 	except:
# 		traceback.print_exc()

def getUserDeviceList(cache,user_id):
	'''
		获取用户所有的设备编号
	'''
	devids = cache.get(base.CacheEntryFormat.UserWithDevice %user_id)
	return devids


