#coding:utf-8

import string
import uuid
from camel.biz.application.camelsrv import CamelApplication,setup,instance
# from camel.fundamental.amqp import AmqpManager
import os.path
from camel.biz.application.camelsrv import CamelApplication,setup,instance
from camel.koala import tcelib as tce
from main import TerminalGatewayServerImpl

class MessageGatewayService(CamelApplication):
    def __init__(self,sid):
        self.mongodb_conn = None
        self.servant = None
        CamelApplication.__init__(self,name=sid)


    def init(self):
        CamelApplication.init(self)
        self._setupRpc()
        self._setupDatabase()

    def _setupDatabase(self):
        # cfg = instance.getConfig().get('database_config',{}).get('mongodb',{})
        # dbname,host,port,user,password = cfg.get('dbname','koala'), cfg.get('host','127.0.0.1'),\
        #         cfg.get('port',27017), cfg.get('user',''), cfg.get('password','')
        # self.mongodb_conn = MongoConnection( dbname,host,port,user,password)
        pass


    def getMongoDatabaseConnection(self):
        return self.mongodb_conn


    def _setupRpc(self):
        loopbacks = []
        eps_listen = []
        path = os.path.join( instance.getConfigPath(),'services.xml')
        tce.RpcCommunicator.instance().init(self.name).initMessageRoute(path)

        server = tce.RpcCommunicator.instance().currentServer()
        value = server.getPropertyValue('listen')
        eps_listen = value.split(',')

        value = server.getPropertyValue('loopback')
        pairs = value.split(',')
        for p in pairs:
            call, return_ = p.split('#')
            loopbacks.append((call, return_))

        servant = TerminalGatewayServerImpl(self)
        for ep in eps_listen:
            ep = ep.strip()
            id = uuid.uuid4().hex
            adapter = tce.RpcCommunicator.instance().createAdapter(id, ep)
            adapter.addServant(servant)

        for lpb in loopbacks:
            lpb = map(string.strip, lpb)
            call, back = lpb
            ep1 = tce.RpcCommunicator.instance().currentServer().findEndPointByName(call)
            ep2 = tce.RpcCommunicator.instance().currentServer().findEndPointByName(back)
            if not ep1 or not ep2:
                print 'error: loopback items <%s> not found!' % str(lpb)
                return -1
            if ep1.type not in ('mq', 'qpid') or ep2.type not in ('mq', 'qpid'):
                print 'error: loopback items <%s> must be mq type!' % str(lpb)
                return -1
            ep1.impl.setLoopbackMQ(ep2.impl) # set recieve mq backway

        # conn_msg = tce.RpcCommunicator.instance().getConnectionMQCollection().get('mq_messageserver')
        # conn_user_event = tce.RpcCommunicator.instance().getConnectionMQCollection().get('mq_user_event_listener')
        #
        # self.servant = MessagingServiceImpl(self)
        #
        # adapter = tce.RpcAdapterMQ.create('mexs', conn_msg)
        # adapter.addConnection(conn_user_event)
        # adapter.addServant(self.servant)


    def _initBefore(self):
        self.config_file = 'settings_mgws.yaml'

    def _setupAmqp(self):
        pass

    def _initSignal(self):pass

    def _setupKafka(self):pass
    def _setupCelery(self):pass
    def _setupZk(self):pass

    def run(self):
        instance.getLogger().info('MGWS Service Started. Name:{}'.format(self.name))
        instance.getLogger().info('Waiting for shutdown..')
        tce.RpcCommunicator.instance().waitForShutdown()

    def _initOptions(self):
        pass

    def _terminate(self):
        # AmqpManager.instance().terminate()
        CamelApplication._terminate(self)

# setup(MessageGatewayService).run()
Server = MessageGatewayService

def run(sid=''):
    Server(sid).run()





