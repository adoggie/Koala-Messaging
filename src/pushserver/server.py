#--coding:utf-8--


import os,sys,traceback,os.path,logging

logging.basicConfig()

PATH = os.path.dirname(os.path.abspath(__file__))
if os.path.exists('%s/../common'%PATH):
	sys.path.append('%s/../common'%PATH)
elif os.path.exists('%s/../../common'%PATH):
	sys.path.append('%s/../../common'%PATH)
else:
	sys.path.append('%s/../../../common'%PATH)

import init_script

from gevent import monkey
monkey.patch_all()

from project import settings
if settings.datebase_is_pgsql():
	import psycogreen.gevent
	psycogreen.gevent.patch_psycopg()

from gevent.pywsgi import WSGIServer
import django
from django.core.handlers.wsgi import WSGIHandler
# 大坑呢 ,  django 1.8+版本必须加上一下代码行,不然出莫名错误
django.setup()

import getopt

import desert
from desert import app
import service.config
from mexs import mexs


class ServerApp( app.BaseAppServer ):
	app.BaseAppServer.init_script = init_script

	def __init__(self,name):
		app.BaseAppServer.__init__(self,name)
		# self.prxMsgServer = None
		# self.CACHE_ENABLE = 0
		# self.NOSQL_ENABLE = 0
		# self.RPC_ENABLE = 0

	def initRpc(self):
		return
		# return
		# app.BaseAppServer.initRpc(self)
		#- 建立与mexs的链接
		# local = self.getEndPointConnection('mq_webserver')
		# connMsgServer = self.getEndPointConnection('mq_messageserver')
		# connMsgServer.setLoopbackMQ(local)
		# # self.prxMsgServer = IMessageServerPrx(connMsgServer)

	# def getProxyMessageServer(self):
	# 	return self.prxMsgServer

	def initNosql(self):
		return
		# app.BaseAppServer.initNosql(self)
		desert.nosql.database = self.mongo.db
		pass

	def initCache(self):
		app.BaseAppServer.initCache(self)
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
				self.getLogger().addHandler( app.BaseAppServer.LOGCLS.StdoutHandler(sys.stdout))
			value = cfg.get('file')
			if value:
				self.getLogger().addHandler(app.BaseAppServer.LOGCLS.FileHandler(value))
			value = cfg.get('dgram')
			if value:
				self.getLogger().addHandler(app.BaseAppServer.LOGCLS.DatagramHandler(value))
		if self.getLogger().handlers:
			sys.stdout = self.getLogger()

	def run(self):

		service.config.initialize(self)
		self.init(init_script.GLOBAL_SETTINGS_FILE,init_script.GLOBAL_SERVICE_FILE)

		self.initLogs()
		# self.initDatabase()

		#- init http service
		cfg = self.conf['http']
		host= cfg['host']
		if not host:
			host = ''
		address = (host,cfg['port'])
		ssl = cfg['ssl']
		app.BaseAppServer.run(self)
		if ssl:
			print 'Webservice Serving [SSL] on %s...'%str(address)
			WSGIServer(address, WSGIHandler(),keyfile=cfg['keyfile'],certfile=cfg['certfile']).serve_forever()
		print 'WebService serving on %s...'%str(address)
		WSGIServer(address, WSGIHandler()).serve_forever()
		# WSGIServer(address, get_wsgi_application() ).serve_forever()


def usage():
	pass

if __name__ == '__main__':
	"""
	mexs.py
		-h
		help
		-n xxx
		--name=xxx
	"""

	servername = 'push_server'
	try:
		options,args = getopt.getopt(sys.argv[1:],'hn:',['help','name='])
		for name,value in options:
			if name in ['-h',"--help"]:
				usage()
				sys.exit()
			if name in ('-n','--name'):
				servername = value

		mexs.ServerAppMexs.instance().init()
		# mexs.ServerAppMexs().init()

		print 'server name:',servername
		ServerApp(servername).run()
	except:
		traceback.print_exc()
		sys.exit()
