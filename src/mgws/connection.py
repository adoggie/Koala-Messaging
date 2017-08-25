#coding:utf-8

import time
import traceback

from camel.biz.application.camelsrv import instance
from camel.koala import tcelib as tce
from camel.koala.koala import ITerminalGatewayServer,IUserEventListenerPrx,ITerminalPrx,Message_t

from camel.koala.errors import ErrorDefs
from camel.koala.token import  decode_user_token
from camel.fundamental.utils.useful import ObjectBuilder


class EventListener(tce.RpcConnectionEventListener):
    def __init__(self,server):
        tce.RpcConnectionEventListener.__init__(self)
        self.server = server


    def isTokenSessionExpired(self,auth):
        """
            是否token会话信息过期
        """
        # expire_time = instance.getConfig().get('access_token_duration',USERTOKEN_EXPIRE_TIME_DEFAULT)
        if time.time() < auth.expire_time:
            return False
        return True

    def connectReject(self,error,conn):
        """
            发送通知到前端设备
        """
        try:
            termPrx = ITerminalPrx(conn)
            msg = Message_t()
            # msg.props = dict( __error__ = ErrorDefs.UserAnotherPlaceLogin.value)
            msg.props = dict( __error__ = error.value,__error_msg__= 'connectReject')
            termPrx.onMessage_oneway(msg)
            conn.close()
        except:
            instance.getLogger().error( traceback.print_exc() )

    def decodeUserToken(self,token):
        token_secret = instance.getConfig().get('token_secret_key','abc123')
        auth = decode_user_token(token,token_secret)
        return ObjectBuilder.create(auth)

    def onDataPacket(self, conn, m):
        '''
            接收到第一个消息包进行检测
            1.检查token是否合法 ( token 有效，且未过期)

            @return:
                False - tce将关闭connection
                True - okay
        '''
        if conn.getRecvedMessageCount() == 1:
            error = None
            # 将 token 直接作为 user_id
            token = m.extra.getValue('__token__')
            if token:
                auth = self.decodeUserToken( token )
                if auth:
                    if self.isTokenSessionExpired(auth):
                        error = ErrorDefs.UserTokenSessionExpired
                    else:
                        # userid = auth.user_id
                        # conn.setUserId(int(userid))
                        # userid = token
                        userid = auth.user_id
                        conn.setUserId(userid)
                        self.server.onUserOnline(userid,'',conn)
                        # print 'user check passed, user:',auth.user_id,auth.user_name
                        print 'user check passed, user:',token
                else:
                    error = ErrorDefs.TicketInvalid
            else:
                error = ErrorDefs.TicketInvalid

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
