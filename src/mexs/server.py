#coding:utf-8

import os.path
import gevent
from camel.biz.application.camelsrv import CamelApplication,setup,instance
from camel.fundamental.amqp import AmqpManager,AccessMode
from camel.fundamental.nosql.mongo import MongoConnection
from camel.koala import tcelib as tce
from .mexs import MessagingServiceImpl

class MessageExchangeServer(CamelApplication):
    def __init__(self,sid):
        self.mongodb_conn = None
        self.servant = None
        CamelApplication.__init__(self,name=sid)


    def init(self):
        CamelApplication.init(self)
        self._setupRpc()
        self._setupDatabase()

    def _setupDatabase(self):
        cfg = instance.getConfig().get('database_config',{}).get('mongodb',{})
        dbname,host,port,user,password = cfg.get('dbname','koala'), cfg.get('host','127.0.0.1'),\
                cfg.get('port',27017), cfg.get('user',''), cfg.get('password','')
        self.mongodb_conn = MongoConnection( dbname,host,port,user,password)

    def getMongoDatabaseConnection(self):
        return self.mongodb_conn


    def _setupRpc(self):
        path = os.path.join( instance.getConfigPath(),'config.yaml')
        tce.RpcCommunicator.instance().init('koala_mexs').initMQEndpoints(path)


        conn_msg = tce.RpcCommunicator.instance().getConnectionMQCollection().get('mq_messageserver')
        conn_user_event = tce.RpcCommunicator.instance().getConnectionMQCollection().get('mq_user_event_listener')

        self.servant = MessagingServiceImpl(self)

        adapter = tce.RpcAdapterMQ.create('mexs', conn_msg,conn_user_event)

        adapter.addServant(self.servant)


    def _initBefore(self):
        self.config_file = 'settings_mexs.yaml'

    def _initSignal(self): pass

    def _setupAmqp(self):
        pass

    def _setupKafka(self):pass
    def _setupCelery(self):pass
    def _setupZk(self):pass

    def run(self):
        instance.getLogger().info('MEXS Service Started.')
        # gevent.sleep(1000000)
        tce.RpcCommunicator.instance().waitForShutdown()
        # CamelApplication.run(self)

    def _terminate(self):
        AmqpManager.instance().terminate()
        CamelApplication._terminate(self)

# setup(MessageExchangeServer).run()

Server = MessageExchangeServer

def run(sid=''):
    Server(sid).run()


"""
HOWTO:
========
python seerver.py -s mgws -i gateway_server

"""
