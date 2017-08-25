#coding:utf-8

import os.path
from camel.biz.application.flasksrv import ServiceFlaskApplication,setup,instance
from camel.fundamental.amqp import AmqpManager,AccessMode
from camel.fundamental.nosql.mongo import MongoConnection
from camel.koala import tcelib as tce
from camel.koala.connection import DatabaseConnectionPool

from camel.koala.koala import IMessageServerPrx

class MessageApplictionService(ServiceFlaskApplication):
    def __init__(self,sid):
        self.prx_mexs = None
        self.mongodb_conn = None
        ServiceFlaskApplication.__init__(self,name=sid)

    def init(self):
        ServiceFlaskApplication.init(self)
        self._setupRpc()
        self._setupDatabase()

    def _setupDatabase(self):
        # self.db_pool = DatabaseConnectionPool(self.getConfig().get('database_config',{}))
        cfg = instance.getConfig().get('database_config',{}).get('mongodb',{})
        dbname,host,port,user,password = cfg.get('dbname','koala'), cfg.get('host','127.0.0.1'),\
                cfg.get('port',27017), cfg.get('user',''), cfg.get('password','')
        self.mongodb_conn = MongoConnection( dbname,host,port,user,password)
        print self.mongodb_conn
        print self.getMongoDatabaseConnection()

    def _initSignal(self):
        pass

    def getMongoDatabaseConnection(self):
        return self.mongodb_conn

    # def getDatabasePool(self):
    #     return self.db_pool

    def _setupRpc(self):
        path = os.path.join( instance.getConfigPath(),'config.yaml')
        tce.RpcCommunicator.instance().init('koala_mas').initMQEndpoints(path)

        conn = tce.RpcCommunicator.instance().getConnectionMQCollection().get('mq_messageserver')
        self.prx_mexs = IMessageServerPrx(conn)


    def _initBefore(self):
        self.config_file = 'settings_mas.yaml'

    def _setupAmqp(self):
        pass

    def _setupKafka(self):pass
    def _setupCelery(self):pass
    def _setupZk(self):pass

    def run(self):
        ServiceFlaskApplication.run(self)

    def getMessageServerProxy(self):
        """ 返回消息交换服务的访问代理对象

        :return:
        """
        return self.prx_mexs


    def _terminate(self):
        ServiceFlaskApplication._terminate(self)

Server = MessageApplictionService

def run(sid=''):
    Server(sid).run()
