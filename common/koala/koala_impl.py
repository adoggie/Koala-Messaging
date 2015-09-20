
# -- coding:utf-8 --

#---------------------------------
#  TCE
#  Tiny Communication Engine
#
#  sw2us.com copyright @2012
#  bin.zhang@sw2us.com / qq:24509826
#---------------------------------

import os,os.path,sys,struct,time,traceback,time
import tcelib as tce

	
class SIDS_t:
	# -- SEQUENCE --
	def __init__(self,array):
		self.ds = array
		
	def marshall(self):
		d = '' 
		d += struct.pack('!I',len(self.ds))
		for o in self.ds:
			d = tce.serial_string(o,d)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			size_,= struct.unpack('!I',d[idx:idx+4])
			idx += 4
			p = 0
			while p < size_:
				v,idx = tce.unserial_string(d,idx)
				self.ds.append(v)
				p+=1
		except:
			traceback.print_exc()
			return False,idx
		return True,idx

class Error_t:
# -- STRUCT -- 
	def __init__(self,succ=False,code=0,msg=''):
		self.succ = succ
		self.code = code
		self.msg = msg
		
	def __str__(self):
		return 'OBJECT<Error_t :%s> { succ:%s,code:%s,msg:%s}'%(hex(id(self)),str(self.succ),str(self.code),str(self.msg) ) 
		
	def marshall(self):
		d =''
		d = tce.serial_bool(self.succ,d)
		d += tce.serial_int(self.code,d)
		d = tce.serial_string(self.msg,d)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			self.succ,idx = tce.unserial_bool(d,idx)
			self.code,idx = tce.unserial_int(d,idx)
			self.msg,idx = tce.unserial_string(d,idx)
		except:
			traceback.print_exc()
			return False,idx
		return True,idx
		

class CallReturn_t:
# -- STRUCT -- 
	def __init__(self,error=Error_t(),value='',delta=''):
		self.error = error
		self.value = value
		self.delta = delta
		
	def __str__(self):
		return 'OBJECT<CallReturn_t :%s> { error:%s,value:%s,delta:%s}'%(hex(id(self)),str(self.error),str(self.value),str(self.delta) ) 
		
	def marshall(self):
		d =''
		d += self.error.marshall()
		d = tce.serial_string(self.value,d)
		d = tce.serial_string(self.delta,d)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			r,idx = self.error.unmarshall(d,idx)
			if not r: return False,idx
			self.value,idx = tce.unserial_string(d,idx)
			self.delta,idx = tce.unserial_string(d,idx)
		except:
			traceback.print_exc()
			return False,idx
		return True,idx
		

class TimeRange_t:
# -- STRUCT -- 
	def __init__(self,start=0,end=0):
		self.start = start
		self.end = end
		
	def __str__(self):
		return 'OBJECT<TimeRange_t :%s> { start:%s,end:%s}'%(hex(id(self)),str(self.start),str(self.end) ) 
		
	def marshall(self):
		d =''
		d = tce.serial_long(self.start,d)
		d = tce.serial_long(self.end,d)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			self.start,idx = tce.unserial_long(d,idx)
			self.end,idx = tce.unserial_long(d,idx)
		except:
			traceback.print_exc()
			return False,idx
		return True,idx
		

class AuthToken_t:
# -- STRUCT -- 
	def __init__(self,user_id='',user_name='',login_time=0,expire_time=0,platform_type=0,device_id=''):
		self.user_id = user_id
		self.user_name = user_name
		self.login_time = login_time
		self.expire_time = expire_time
		self.platform_type = platform_type
		self.device_id = device_id
		
	def __str__(self):
		return 'OBJECT<AuthToken_t :%s> { user_id:%s,user_name:%s,login_time:%s,expire_time:%s,platform_type:%s,device_id:%s}'%(hex(id(self)),str(self.user_id),str(self.user_name),str(self.login_time),str(self.expire_time),str(self.platform_type),str(self.device_id) ) 
		
	def marshall(self):
		d =''
		d = tce.serial_string(self.user_id,d)
		d = tce.serial_string(self.user_name,d)
		d = tce.serial_long(self.login_time,d)
		d = tce.serial_long(self.expire_time,d)
		d += tce.serial_int(self.platform_type,d)
		d = tce.serial_string(self.device_id,d)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			self.user_id,idx = tce.unserial_string(d,idx)
			self.user_name,idx = tce.unserial_string(d,idx)
			self.login_time,idx = tce.unserial_long(d,idx)
			self.expire_time,idx = tce.unserial_long(d,idx)
			self.platform_type,idx = tce.unserial_int(d,idx)
			self.device_id,idx = tce.unserial_string(d,idx)
		except:
			traceback.print_exc()
			return False,idx
		return True,idx
		

class MessageStyle_t:
# -- STRUCT -- 
	def __init__(self,builder_id=0,ring=0):
		self.builder_id = builder_id
		self.ring = ring
		
	def __str__(self):
		return 'OBJECT<MessageStyle_t :%s> { builder_id:%s,ring:%s}'%(hex(id(self)),str(self.builder_id),str(self.ring) ) 
		
	def marshall(self):
		d =''
		d += tce.serial_int(self.builder_id,d)
		d += tce.serial_int(self.ring,d)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			self.builder_id,idx = tce.unserial_int(d,idx)
			self.ring,idx = tce.unserial_int(d,idx)
		except:
			traceback.print_exc()
			return False,idx
		return True,idx
		

class ClickAction_t:
# -- STRUCT -- 
	def __init__(self,act_type=0,url='',conform_on_url=0,activity='',intent='',intent_flag=0,pending_flag=0,package_name='',package_download_url='',confirm_on_package=0):
		self.act_type = act_type
		self.url = url
		self.conform_on_url = conform_on_url
		self.activity = activity
		self.intent = intent
		self.intent_flag = intent_flag
		self.pending_flag = pending_flag
		self.package_name = package_name
		self.package_download_url = package_download_url
		self.confirm_on_package = confirm_on_package
		
	def __str__(self):
		return 'OBJECT<ClickAction_t :%s> { act_type:%s,url:%s,conform_on_url:%s,activity:%s,intent:%s,intent_flag:%s,pending_flag:%s,package_name:%s,package_download_url:%s,confirm_on_package:%s}'%(hex(id(self)),str(self.act_type),str(self.url),str(self.conform_on_url),str(self.activity),str(self.intent),str(self.intent_flag),str(self.pending_flag),str(self.package_name),str(self.package_download_url),str(self.confirm_on_package) ) 
		
	def marshall(self):
		d =''
		d += tce.serial_int(self.act_type,d)
		d = tce.serial_string(self.url,d)
		d += tce.serial_int(self.conform_on_url,d)
		d = tce.serial_string(self.activity,d)
		d = tce.serial_string(self.intent,d)
		d += tce.serial_int(self.intent_flag,d)
		d += tce.serial_int(self.pending_flag,d)
		d = tce.serial_string(self.package_name,d)
		d = tce.serial_string(self.package_download_url,d)
		d += tce.serial_int(self.confirm_on_package,d)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			self.act_type,idx = tce.unserial_int(d,idx)
			self.url,idx = tce.unserial_string(d,idx)
			self.conform_on_url,idx = tce.unserial_int(d,idx)
			self.activity,idx = tce.unserial_string(d,idx)
			self.intent,idx = tce.unserial_string(d,idx)
			self.intent_flag,idx = tce.unserial_int(d,idx)
			self.pending_flag,idx = tce.unserial_int(d,idx)
			self.package_name,idx = tce.unserial_string(d,idx)
			self.package_download_url,idx = tce.unserial_string(d,idx)
			self.confirm_on_package,idx = tce.unserial_int(d,idx)
		except:
			traceback.print_exc()
			return False,idx
		return True,idx
		

class SimpleText_t:
# -- STRUCT -- 
	def __init__(self,seq='',sender_id='',send_time='',title='',content=''):
		self.seq = seq
		self.sender_id = sender_id
		self.send_time = send_time
		self.title = title
		self.content = content
		
	def __str__(self):
		return 'OBJECT<SimpleText_t :%s> { seq:%s,sender_id:%s,send_time:%s,title:%s,content:%s}'%(hex(id(self)),str(self.seq),str(self.sender_id),str(self.send_time),str(self.title),str(self.content) ) 
		
	def marshall(self):
		d =''
		d = tce.serial_string(self.seq,d)
		d = tce.serial_string(self.sender_id,d)
		d = tce.serial_string(self.send_time,d)
		d = tce.serial_string(self.title,d)
		d = tce.serial_string(self.content,d)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			self.seq,idx = tce.unserial_string(d,idx)
			self.sender_id,idx = tce.unserial_string(d,idx)
			self.send_time,idx = tce.unserial_string(d,idx)
			self.title,idx = tce.unserial_string(d,idx)
			self.content,idx = tce.unserial_string(d,idx)
		except:
			traceback.print_exc()
			return False,idx
		return True,idx
		

class Message_t:
# -- STRUCT -- 
	def __init__(self,seq='',sender_id='',sent_time='',title='',content='',expire_time='',send_time='',accept_time='',type_=0,style=MessageStyle_t(),action=ClickAction_t(),custom='',loop_times=0,loop_inerval=0,alert='',badge=0,sound='',category='',raw=''):
		self.seq = seq
		self.sender_id = sender_id
		self.sent_time = sent_time
		self.title = title
		self.content = content
		self.expire_time = expire_time
		self.send_time = send_time
		self.accept_time = accept_time
		self.type_ = type_
		self.style = style
		self.action = action
		self.custom = custom
		self.loop_times = loop_times
		self.loop_inerval = loop_inerval
		self.alert = alert
		self.badge = badge
		self.sound = sound
		self.category = category
		self.raw = raw
		
	def __str__(self):
		return 'OBJECT<Message_t :%s> { seq:%s,sender_id:%s,sent_time:%s,title:%s,content:%s,expire_time:%s,send_time:%s,accept_time:%s,type_:%s,style:%s,action:%s,custom:%s,loop_times:%s,loop_inerval:%s,alert:%s,badge:%s,sound:%s,category:%s,raw:%s}'%(hex(id(self)),str(self.seq),str(self.sender_id),str(self.sent_time),str(self.title),str(self.content),str(self.expire_time),str(self.send_time),str(self.accept_time),str(self.type_),str(self.style),str(self.action),str(self.custom),str(self.loop_times),str(self.loop_inerval),str(self.alert),str(self.badge),str(self.sound),str(self.category),str(self.raw) ) 
		
	def marshall(self):
		d =''
		d = tce.serial_string(self.seq,d)
		d = tce.serial_string(self.sender_id,d)
		d = tce.serial_string(self.sent_time,d)
		d = tce.serial_string(self.title,d)
		d = tce.serial_string(self.content,d)
		d = tce.serial_string(self.expire_time,d)
		d = tce.serial_string(self.send_time,d)
		d = tce.serial_string(self.accept_time,d)
		d += tce.serial_int(self.type_,d)
		d += self.style.marshall()
		d += self.action.marshall()
		d = tce.serial_string(self.custom,d)
		d += tce.serial_int(self.loop_times,d)
		d += tce.serial_int(self.loop_inerval,d)
		d = tce.serial_string(self.alert,d)
		d += tce.serial_int(self.badge,d)
		d = tce.serial_string(self.sound,d)
		d = tce.serial_string(self.category,d)
		d = tce.serial_string(self.raw,d)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			self.seq,idx = tce.unserial_string(d,idx)
			self.sender_id,idx = tce.unserial_string(d,idx)
			self.sent_time,idx = tce.unserial_string(d,idx)
			self.title,idx = tce.unserial_string(d,idx)
			self.content,idx = tce.unserial_string(d,idx)
			self.expire_time,idx = tce.unserial_string(d,idx)
			self.send_time,idx = tce.unserial_string(d,idx)
			self.accept_time,idx = tce.unserial_string(d,idx)
			self.type_,idx = tce.unserial_int(d,idx)
			r,idx = self.style.unmarshall(d,idx)
			if not r: return False,idx
			r,idx = self.action.unmarshall(d,idx)
			if not r: return False,idx
			self.custom,idx = tce.unserial_string(d,idx)
			self.loop_times,idx = tce.unserial_int(d,idx)
			self.loop_inerval,idx = tce.unserial_int(d,idx)
			self.alert,idx = tce.unserial_string(d,idx)
			self.badge,idx = tce.unserial_int(d,idx)
			self.sound,idx = tce.unserial_string(d,idx)
			self.category,idx = tce.unserial_string(d,idx)
			self.raw,idx = tce.unserial_string(d,idx)
		except:
			traceback.print_exc()
			return False,idx
		return True,idx
		

class Notification_t:
# -- STRUCT -- 
	def __init__(self,type_='',title='',content='',p1='',p2=''):
		self.type_ = type_
		self.title = title
		self.content = content
		self.p1 = p1
		self.p2 = p2
		
	def __str__(self):
		return 'OBJECT<Notification_t :%s> { type_:%s,title:%s,content:%s,p1:%s,p2:%s}'%(hex(id(self)),str(self.type_),str(self.title),str(self.content),str(self.p1),str(self.p2) ) 
		
	def marshall(self):
		d =''
		d = tce.serial_string(self.type_,d)
		d = tce.serial_string(self.title,d)
		d = tce.serial_string(self.content,d)
		d = tce.serial_string(self.p1,d)
		d = tce.serial_string(self.p2,d)
		return d
		
	def unmarshall(self,d,idx_=0):
		idx = idx_
		try:
			self.type_,idx = tce.unserial_string(d,idx)
			self.title,idx = tce.unserial_string(d,idx)
			self.content,idx = tce.unserial_string(d,idx)
			self.p1,idx = tce.unserial_string(d,idx)
			self.p2,idx = tce.unserial_string(d,idx)
		except:
			traceback.print_exc()
			return False,idx
		return True,idx
		

class ITerminal(tce.RpcServantBase):
	# -- INTERFACE -- 
	def __init__(self):
		tce.RpcServantBase.__init__(self)
		if not hasattr(self,'delegatecls'):
			self.delegatecls = {}
		self.delegatecls[0] = ITerminal_delegate
	
	def onSimpleText(self,text,ctx):
		pass
	
	def onMessage(self,message,ctx):
		pass
	
	def onError(self,errcode,errmsg,ctx):
		pass
	
	def onSystemNotification(self,notification,ctx):
		pass
	

class ITerminal_delegate:
	def __init__(self,inst,adapter,conn=None):
		self.index = 0
		self.optlist={}
		self.id = '' 
		self.adapter = adapter
		self.optlist[0] = self.onSimpleText
		self.optlist[1] = self.onMessage
		self.optlist[2] = self.onError
		self.optlist[3] = self.onSystemNotification
		
		self.inst = inst
	
	def onSimpleText(self,ctx):
		tce.log_debug("callin (onSimpleText)")
		d = ctx.msg.paramstream 
		idx = 0
		_p_text = SimpleText_t()
		r,idx = _p_text.unmarshall(d,idx)
		if not r: return False
		cr = None
		self.inst.onSimpleText(_p_text,ctx)
		if ctx.msg.calltype & tce.RpcMessage.ONEWAY: return True
		d = '' 
		m = tce.RpcMessageReturn(self.inst)
		m.sequence = ctx.msg.sequence
		m.callmsg = ctx.msg
		m.ifidx = ctx.msg.ifidx
		m.call_id = ctx.msg.call_id
		m.conn = ctx.msg.conn
		m.extra = ctx.msg.extra
		if d: m.paramstream += d
		ctx.conn.sendMessage(m)
		return True
	
	def onMessage(self,ctx):
		tce.log_debug("callin (onMessage)")
		d = ctx.msg.paramstream 
		idx = 0
		_p_message = Message_t()
		r,idx = _p_message.unmarshall(d,idx)
		if not r: return False
		cr = None
		self.inst.onMessage(_p_message,ctx)
		if ctx.msg.calltype & tce.RpcMessage.ONEWAY: return True
		d = '' 
		m = tce.RpcMessageReturn(self.inst)
		m.sequence = ctx.msg.sequence
		m.callmsg = ctx.msg
		m.ifidx = ctx.msg.ifidx
		m.call_id = ctx.msg.call_id
		m.conn = ctx.msg.conn
		m.extra = ctx.msg.extra
		if d: m.paramstream += d
		ctx.conn.sendMessage(m)
		return True
	
	def onError(self,ctx):
		tce.log_debug("callin (onError)")
		d = ctx.msg.paramstream 
		idx = 0
		_p_errcode,idx = tce.unserial_string(d,idx)
		_p_errmsg,idx = tce.unserial_string(d,idx)
		cr = None
		self.inst.onError(_p_errcode,_p_errmsg,ctx)
		if ctx.msg.calltype & tce.RpcMessage.ONEWAY: return True
		d = '' 
		m = tce.RpcMessageReturn(self.inst)
		m.sequence = ctx.msg.sequence
		m.callmsg = ctx.msg
		m.ifidx = ctx.msg.ifidx
		m.call_id = ctx.msg.call_id
		m.conn = ctx.msg.conn
		m.extra = ctx.msg.extra
		if d: m.paramstream += d
		ctx.conn.sendMessage(m)
		return True
	
	def onSystemNotification(self,ctx):
		tce.log_debug("callin (onSystemNotification)")
		d = ctx.msg.paramstream 
		idx = 0
		_p_notification = Notification_t()
		r,idx = _p_notification.unmarshall(d,idx)
		if not r: return False
		cr = None
		self.inst.onSystemNotification(_p_notification,ctx)
		if ctx.msg.calltype & tce.RpcMessage.ONEWAY: return True
		d = '' 
		m = tce.RpcMessageReturn(self.inst)
		m.sequence = ctx.msg.sequence
		m.callmsg = ctx.msg
		m.ifidx = ctx.msg.ifidx
		m.call_id = ctx.msg.call_id
		m.conn = ctx.msg.conn
		m.extra = ctx.msg.extra
		if d: m.paramstream += d
		ctx.conn.sendMessage(m)
		return True
	
	
class ITerminalPrx(tce.RpcProxyBase):
	# -- INTERFACE PROXY -- 
	def __init__(self,conn):
		tce.RpcProxyBase.__init__(self)
		self.conn = conn
		self.delta = None
		pass
	
	@staticmethod
	def create(ep,af= tce.AF_WRITE | tce.AF_READ):
		ep.open(af)
		conn = ep.impl
		proxy = ITerminalPrx(conn)
		return proxy
	
	@staticmethod
	def createWithEpName(name):
		ep = tce.RpcCommunicator.instance().currentServer().findEndPointByName(name)
		if not ep: return None
		conn = ep.impl
		proxy = ITerminalPrx(conn)
		return proxy
	
	@staticmethod
	def createWithProxy(prx):
		proxy = ITerminalPrx(prx.conn)
		return proxy
	
	#extra must be map<string,string>
	def onSimpleText(self,text,timeout=None,extra={}):
		# function index: 10
		
		m_1 = tce.RpcMessageCall(self)
		m_1.ifidx = 0
		m_1.opidx = 0
		m_1.extra.setStrDict(extra)
		d_2 = '' 
		d_2 += text.marshall()
		m_1.paramstream += d_2
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		r_4 = self.conn.sendMessage(m_1)
		if not r_4:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		if not timeout: timeout = tce.RpcCommunicator.instance().getRpcCallTimeout()
		m_5 = None
		try:
			m_5 = m_1.mtx.get(timeout=timeout)
		except:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_TIMEOUT)
		if m_5.errcode != tce.RpcConsts.RPCERROR_SUCC:
			raise tce.RpcException(m_5.errcode)
		m_1 = m_5
	
	def onSimpleText_async(self,text,async,cookie=None,extra={}):
		# function index: 10
		
		ecode_2 = tce.RpcConsts.RPCERROR_SUCC
		m_1 = tce.RpcMessageCall(self)
		m_1.cookie = cookie
		m_1.ifidx = 0
		m_1.opidx = 0
		m_1.extra.setStrDict(extra)
		d_3 = '' 
		d_3 += text.marshall()
		m_1.paramstream += d_3
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		m_1.async = async
		m_1.asyncparser = ITerminalPrx.onSimpleText_asyncparser
		r_5 = self.conn.sendMessage(m_1)
		if not r_5:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	@staticmethod
	def onSimpleText_asyncparser(m,m2):
		# function index: 10 , m2 - callreturn msg.
		
		stream_1 = m2.paramstream
		user_2 = m.async
		prx_3 = m.prx
		if m2.errcode != tce.RpcConsts.RPCERROR_SUCC: return 
		try:
			idx_4 = 0
			d_5 = stream_1
			r_6 = True
			if r_6:
				user_2(prx_3,m.cookie)
		except:
			traceback.print_exc()
		
	
	def onSimpleText_oneway(self,text,extra={}):
		# function index: idx_4
		
		try:
			m_1 = tce.RpcMessageCall(self)
			m_1.ifidx = 0
			m_1.opidx = 0
			m_1.calltype |= tce.RpcMessage.ONEWAY
			m_1.prx = self
			m_1.conn = m_1.prx.conn
			m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
			m_1.extra.setStrDict(extra)
			d_2 = '' 
			d_2 += text.marshall()
			m_1.paramstream += d_2
			r_4 = self.conn.sendMessage(m_1)
			if not r_4:
				raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		except:
			traceback.print_exc()
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	#extra must be map<string,string>
	def onMessage(self,message,timeout=None,extra={}):
		# function index: idx_4
		
		m_1 = tce.RpcMessageCall(self)
		m_1.ifidx = 0
		m_1.opidx = 1
		m_1.extra.setStrDict(extra)
		d_2 = '' 
		d_2 += message.marshall()
		m_1.paramstream += d_2
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		r_4 = self.conn.sendMessage(m_1)
		if not r_4:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		if not timeout: timeout = tce.RpcCommunicator.instance().getRpcCallTimeout()
		m_5 = None
		try:
			m_5 = m_1.mtx.get(timeout=timeout)
		except:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_TIMEOUT)
		if m_5.errcode != tce.RpcConsts.RPCERROR_SUCC:
			raise tce.RpcException(m_5.errcode)
		m_1 = m_5
	
	def onMessage_async(self,message,async,cookie=None,extra={}):
		# function index: idx_4
		
		ecode_2 = tce.RpcConsts.RPCERROR_SUCC
		m_1 = tce.RpcMessageCall(self)
		m_1.cookie = cookie
		m_1.ifidx = 0
		m_1.opidx = 1
		m_1.extra.setStrDict(extra)
		d_3 = '' 
		d_3 += message.marshall()
		m_1.paramstream += d_3
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		m_1.async = async
		m_1.asyncparser = ITerminalPrx.onMessage_asyncparser
		r_5 = self.conn.sendMessage(m_1)
		if not r_5:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	@staticmethod
	def onMessage_asyncparser(m,m2):
		# function index: idx_4 , m2 - callreturn msg.
		
		stream_1 = m2.paramstream
		user_2 = m.async
		prx_3 = m.prx
		if m2.errcode != tce.RpcConsts.RPCERROR_SUCC: return 
		try:
			idx_4 = 0
			d_5 = stream_1
			r_6 = True
			if r_6:
				user_2(prx_3,m.cookie)
		except:
			traceback.print_exc()
		
	
	def onMessage_oneway(self,message,extra={}):
		# function index: idx_4
		
		try:
			m_1 = tce.RpcMessageCall(self)
			m_1.ifidx = 0
			m_1.opidx = 1
			m_1.calltype |= tce.RpcMessage.ONEWAY
			m_1.prx = self
			m_1.conn = m_1.prx.conn
			m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
			m_1.extra.setStrDict(extra)
			d_2 = '' 
			d_2 += message.marshall()
			m_1.paramstream += d_2
			r_4 = self.conn.sendMessage(m_1)
			if not r_4:
				raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		except:
			traceback.print_exc()
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	#extra must be map<string,string>
	def onError(self,errcode,errmsg,timeout=None,extra={}):
		# function index: idx_4
		
		m_1 = tce.RpcMessageCall(self)
		m_1.ifidx = 0
		m_1.opidx = 2
		m_1.extra.setStrDict(extra)
		d_2 = '' 
		d_2 = tce.serial_string(errcode,d_2)
		m_1.paramstream += d_2
		d_2 = '' 
		d_2 = tce.serial_string(errmsg,d_2)
		m_1.paramstream += d_2
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		r_4 = self.conn.sendMessage(m_1)
		if not r_4:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		if not timeout: timeout = tce.RpcCommunicator.instance().getRpcCallTimeout()
		m_5 = None
		try:
			m_5 = m_1.mtx.get(timeout=timeout)
		except:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_TIMEOUT)
		if m_5.errcode != tce.RpcConsts.RPCERROR_SUCC:
			raise tce.RpcException(m_5.errcode)
		m_1 = m_5
	
	def onError_async(self,errcode,errmsg,async,cookie=None,extra={}):
		# function index: idx_4
		
		ecode_2 = tce.RpcConsts.RPCERROR_SUCC
		m_1 = tce.RpcMessageCall(self)
		m_1.cookie = cookie
		m_1.ifidx = 0
		m_1.opidx = 2
		m_1.extra.setStrDict(extra)
		d_3 = '' 
		d_3 = tce.serial_string(errcode,d_3)
		m_1.paramstream += d_3
		d_3 = '' 
		d_3 = tce.serial_string(errmsg,d_3)
		m_1.paramstream += d_3
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		m_1.async = async
		m_1.asyncparser = ITerminalPrx.onError_asyncparser
		r_5 = self.conn.sendMessage(m_1)
		if not r_5:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	@staticmethod
	def onError_asyncparser(m,m2):
		# function index: idx_4 , m2 - callreturn msg.
		
		stream_1 = m2.paramstream
		user_2 = m.async
		prx_3 = m.prx
		if m2.errcode != tce.RpcConsts.RPCERROR_SUCC: return 
		try:
			idx_4 = 0
			d_5 = stream_1
			r_6 = True
			if r_6:
				user_2(prx_3,m.cookie)
		except:
			traceback.print_exc()
		
	
	def onError_oneway(self,errcode,errmsg,extra={}):
		# function index: idx_4
		
		try:
			m_1 = tce.RpcMessageCall(self)
			m_1.ifidx = 0
			m_1.opidx = 2
			m_1.calltype |= tce.RpcMessage.ONEWAY
			m_1.prx = self
			m_1.conn = m_1.prx.conn
			m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
			m_1.extra.setStrDict(extra)
			d_2 = '' 
			d_2 = tce.serial_string(errcode,d_2)
			m_1.paramstream += d_2
			d_2 = '' 
			d_2 = tce.serial_string(errmsg,d_2)
			m_1.paramstream += d_2
			r_4 = self.conn.sendMessage(m_1)
			if not r_4:
				raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		except:
			traceback.print_exc()
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	#extra must be map<string,string>
	def onSystemNotification(self,notification,timeout=None,extra={}):
		# function index: idx_4
		
		m_1 = tce.RpcMessageCall(self)
		m_1.ifidx = 0
		m_1.opidx = 3
		m_1.extra.setStrDict(extra)
		d_2 = '' 
		d_2 += notification.marshall()
		m_1.paramstream += d_2
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		r_4 = self.conn.sendMessage(m_1)
		if not r_4:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		if not timeout: timeout = tce.RpcCommunicator.instance().getRpcCallTimeout()
		m_5 = None
		try:
			m_5 = m_1.mtx.get(timeout=timeout)
		except:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_TIMEOUT)
		if m_5.errcode != tce.RpcConsts.RPCERROR_SUCC:
			raise tce.RpcException(m_5.errcode)
		m_1 = m_5
	
	def onSystemNotification_async(self,notification,async,cookie=None,extra={}):
		# function index: idx_4
		
		ecode_2 = tce.RpcConsts.RPCERROR_SUCC
		m_1 = tce.RpcMessageCall(self)
		m_1.cookie = cookie
		m_1.ifidx = 0
		m_1.opidx = 3
		m_1.extra.setStrDict(extra)
		d_3 = '' 
		d_3 += notification.marshall()
		m_1.paramstream += d_3
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		m_1.async = async
		m_1.asyncparser = ITerminalPrx.onSystemNotification_asyncparser
		r_5 = self.conn.sendMessage(m_1)
		if not r_5:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	@staticmethod
	def onSystemNotification_asyncparser(m,m2):
		# function index: idx_4 , m2 - callreturn msg.
		
		stream_1 = m2.paramstream
		user_2 = m.async
		prx_3 = m.prx
		if m2.errcode != tce.RpcConsts.RPCERROR_SUCC: return 
		try:
			idx_4 = 0
			d_5 = stream_1
			r_6 = True
			if r_6:
				user_2(prx_3,m.cookie)
		except:
			traceback.print_exc()
		
	
	def onSystemNotification_oneway(self,notification,extra={}):
		# function index: idx_4
		
		try:
			m_1 = tce.RpcMessageCall(self)
			m_1.ifidx = 0
			m_1.opidx = 3
			m_1.calltype |= tce.RpcMessage.ONEWAY
			m_1.prx = self
			m_1.conn = m_1.prx.conn
			m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
			m_1.extra.setStrDict(extra)
			d_2 = '' 
			d_2 += notification.marshall()
			m_1.paramstream += d_2
			r_4 = self.conn.sendMessage(m_1)
			if not r_4:
				raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		except:
			traceback.print_exc()
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	

class IUserEventListener(tce.RpcServantBase):
	# -- INTERFACE -- 
	def __init__(self):
		tce.RpcServantBase.__init__(self)
		if not hasattr(self,'delegatecls'):
			self.delegatecls = {}
		self.delegatecls[1] = IUserEventListener_delegate
	
	def onUserOnline(self,userid,gws_id,device,ctx):
		pass
	
	def onUserOffline(self,userid,gws_id,device,ctx):
		pass
	

class IUserEventListener_delegate:
	def __init__(self,inst,adapter,conn=None):
		self.index = 1
		self.optlist={}
		self.id = '' 
		self.adapter = adapter
		self.optlist[0] = self.onUserOnline
		self.optlist[1] = self.onUserOffline
		
		self.inst = inst
	
	def onUserOnline(self,ctx):
		tce.log_debug("callin (onUserOnline)")
		d = ctx.msg.paramstream 
		idx = 0
		_p_userid,idx = tce.unserial_string(d,idx)
		_p_gws_id,idx = tce.unserial_string(d,idx)
		_p_device,idx = tce.unserial_int(d,idx)
		cr = None
		self.inst.onUserOnline(_p_userid,_p_gws_id,_p_device,ctx)
		if ctx.msg.calltype & tce.RpcMessage.ONEWAY: return True
		d = '' 
		m = tce.RpcMessageReturn(self.inst)
		m.sequence = ctx.msg.sequence
		m.callmsg = ctx.msg
		m.ifidx = ctx.msg.ifidx
		m.call_id = ctx.msg.call_id
		m.conn = ctx.msg.conn
		m.extra = ctx.msg.extra
		if d: m.paramstream += d
		ctx.conn.sendMessage(m)
		return True
	
	def onUserOffline(self,ctx):
		tce.log_debug("callin (onUserOffline)")
		d = ctx.msg.paramstream 
		idx = 0
		_p_userid,idx = tce.unserial_string(d,idx)
		_p_gws_id,idx = tce.unserial_string(d,idx)
		_p_device,idx = tce.unserial_int(d,idx)
		cr = None
		self.inst.onUserOffline(_p_userid,_p_gws_id,_p_device,ctx)
		if ctx.msg.calltype & tce.RpcMessage.ONEWAY: return True
		d = '' 
		m = tce.RpcMessageReturn(self.inst)
		m.sequence = ctx.msg.sequence
		m.callmsg = ctx.msg
		m.ifidx = ctx.msg.ifidx
		m.call_id = ctx.msg.call_id
		m.conn = ctx.msg.conn
		m.extra = ctx.msg.extra
		if d: m.paramstream += d
		ctx.conn.sendMessage(m)
		return True
	
	
class IUserEventListenerPrx(tce.RpcProxyBase):
	# -- INTERFACE PROXY -- 
	def __init__(self,conn):
		tce.RpcProxyBase.__init__(self)
		self.conn = conn
		self.delta = None
		pass
	
	@staticmethod
	def create(ep,af= tce.AF_WRITE | tce.AF_READ):
		ep.open(af)
		conn = ep.impl
		proxy = IUserEventListenerPrx(conn)
		return proxy
	
	@staticmethod
	def createWithEpName(name):
		ep = tce.RpcCommunicator.instance().currentServer().findEndPointByName(name)
		if not ep: return None
		conn = ep.impl
		proxy = IUserEventListenerPrx(conn)
		return proxy
	
	@staticmethod
	def createWithProxy(prx):
		proxy = IUserEventListenerPrx(prx.conn)
		return proxy
	
	#extra must be map<string,string>
	def onUserOnline(self,userid,gws_id,device,timeout=None,extra={}):
		# function index: 11
		
		m_1 = tce.RpcMessageCall(self)
		m_1.ifidx = 1
		m_1.opidx = 0
		m_1.extra.setStrDict(extra)
		d_2 = '' 
		d_2 = tce.serial_string(userid,d_2)
		m_1.paramstream += d_2
		d_2 = '' 
		d_2 = tce.serial_string(gws_id,d_2)
		m_1.paramstream += d_2
		d_2 = '' 
		d_2 += tce.serial_int(device,d_2)
		m_1.paramstream += d_2
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		r_4 = self.conn.sendMessage(m_1)
		if not r_4:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		if not timeout: timeout = tce.RpcCommunicator.instance().getRpcCallTimeout()
		m_5 = None
		try:
			m_5 = m_1.mtx.get(timeout=timeout)
		except:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_TIMEOUT)
		if m_5.errcode != tce.RpcConsts.RPCERROR_SUCC:
			raise tce.RpcException(m_5.errcode)
		m_1 = m_5
	
	def onUserOnline_async(self,userid,gws_id,device,async,cookie=None,extra={}):
		# function index: 11
		
		ecode_2 = tce.RpcConsts.RPCERROR_SUCC
		m_1 = tce.RpcMessageCall(self)
		m_1.cookie = cookie
		m_1.ifidx = 1
		m_1.opidx = 0
		m_1.extra.setStrDict(extra)
		d_3 = '' 
		d_3 = tce.serial_string(userid,d_3)
		m_1.paramstream += d_3
		d_3 = '' 
		d_3 = tce.serial_string(gws_id,d_3)
		m_1.paramstream += d_3
		d_3 = '' 
		d_3 += tce.serial_int(device,d_3)
		m_1.paramstream += d_3
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		m_1.async = async
		m_1.asyncparser = IUserEventListenerPrx.onUserOnline_asyncparser
		r_5 = self.conn.sendMessage(m_1)
		if not r_5:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	@staticmethod
	def onUserOnline_asyncparser(m,m2):
		# function index: 11 , m2 - callreturn msg.
		
		stream_1 = m2.paramstream
		user_2 = m.async
		prx_3 = m.prx
		if m2.errcode != tce.RpcConsts.RPCERROR_SUCC: return 
		try:
			idx_4 = 0
			d_5 = stream_1
			r_6 = True
			if r_6:
				user_2(prx_3,m.cookie)
		except:
			traceback.print_exc()
		
	
	def onUserOnline_oneway(self,userid,gws_id,device,extra={}):
		# function index: idx_4
		
		try:
			m_1 = tce.RpcMessageCall(self)
			m_1.ifidx = 1
			m_1.opidx = 0
			m_1.calltype |= tce.RpcMessage.ONEWAY
			m_1.prx = self
			m_1.conn = m_1.prx.conn
			m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
			m_1.extra.setStrDict(extra)
			d_2 = '' 
			d_2 = tce.serial_string(userid,d_2)
			m_1.paramstream += d_2
			d_2 = '' 
			d_2 = tce.serial_string(gws_id,d_2)
			m_1.paramstream += d_2
			d_2 = '' 
			d_2 += tce.serial_int(device,d_2)
			m_1.paramstream += d_2
			r_4 = self.conn.sendMessage(m_1)
			if not r_4:
				raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		except:
			traceback.print_exc()
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	#extra must be map<string,string>
	def onUserOffline(self,userid,gws_id,device,timeout=None,extra={}):
		# function index: idx_4
		
		m_1 = tce.RpcMessageCall(self)
		m_1.ifidx = 1
		m_1.opidx = 1
		m_1.extra.setStrDict(extra)
		d_2 = '' 
		d_2 = tce.serial_string(userid,d_2)
		m_1.paramstream += d_2
		d_2 = '' 
		d_2 = tce.serial_string(gws_id,d_2)
		m_1.paramstream += d_2
		d_2 = '' 
		d_2 += tce.serial_int(device,d_2)
		m_1.paramstream += d_2
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		r_4 = self.conn.sendMessage(m_1)
		if not r_4:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		if not timeout: timeout = tce.RpcCommunicator.instance().getRpcCallTimeout()
		m_5 = None
		try:
			m_5 = m_1.mtx.get(timeout=timeout)
		except:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_TIMEOUT)
		if m_5.errcode != tce.RpcConsts.RPCERROR_SUCC:
			raise tce.RpcException(m_5.errcode)
		m_1 = m_5
	
	def onUserOffline_async(self,userid,gws_id,device,async,cookie=None,extra={}):
		# function index: idx_4
		
		ecode_2 = tce.RpcConsts.RPCERROR_SUCC
		m_1 = tce.RpcMessageCall(self)
		m_1.cookie = cookie
		m_1.ifidx = 1
		m_1.opidx = 1
		m_1.extra.setStrDict(extra)
		d_3 = '' 
		d_3 = tce.serial_string(userid,d_3)
		m_1.paramstream += d_3
		d_3 = '' 
		d_3 = tce.serial_string(gws_id,d_3)
		m_1.paramstream += d_3
		d_3 = '' 
		d_3 += tce.serial_int(device,d_3)
		m_1.paramstream += d_3
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		m_1.async = async
		m_1.asyncparser = IUserEventListenerPrx.onUserOffline_asyncparser
		r_5 = self.conn.sendMessage(m_1)
		if not r_5:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	@staticmethod
	def onUserOffline_asyncparser(m,m2):
		# function index: idx_4 , m2 - callreturn msg.
		
		stream_1 = m2.paramstream
		user_2 = m.async
		prx_3 = m.prx
		if m2.errcode != tce.RpcConsts.RPCERROR_SUCC: return 
		try:
			idx_4 = 0
			d_5 = stream_1
			r_6 = True
			if r_6:
				user_2(prx_3,m.cookie)
		except:
			traceback.print_exc()
		
	
	def onUserOffline_oneway(self,userid,gws_id,device,extra={}):
		# function index: idx_4
		
		try:
			m_1 = tce.RpcMessageCall(self)
			m_1.ifidx = 1
			m_1.opidx = 1
			m_1.calltype |= tce.RpcMessage.ONEWAY
			m_1.prx = self
			m_1.conn = m_1.prx.conn
			m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
			m_1.extra.setStrDict(extra)
			d_2 = '' 
			d_2 = tce.serial_string(userid,d_2)
			m_1.paramstream += d_2
			d_2 = '' 
			d_2 = tce.serial_string(gws_id,d_2)
			m_1.paramstream += d_2
			d_2 = '' 
			d_2 += tce.serial_int(device,d_2)
			m_1.paramstream += d_2
			r_4 = self.conn.sendMessage(m_1)
			if not r_4:
				raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		except:
			traceback.print_exc()
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	

class ITerminalGatewayServer(tce.RpcServantBase):
	# -- INTERFACE -- 
	def __init__(self):
		tce.RpcServantBase.__init__(self)
		if not hasattr(self,'delegatecls'):
			self.delegatecls = {}
		self.delegatecls[2] = ITerminalGatewayServer_delegate
	
	def ping(self,ctx):
		pass
	

class ITerminalGatewayServer_delegate:
	def __init__(self,inst,adapter,conn=None):
		self.index = 2
		self.optlist={}
		self.id = '' 
		self.adapter = adapter
		self.optlist[0] = self.ping
		
		self.inst = inst
	
	def ping(self,ctx):
		tce.log_debug("callin (ping)")
		d = ctx.msg.paramstream 
		idx = 0
		cr = None
		self.inst.ping(ctx)
		if ctx.msg.calltype & tce.RpcMessage.ONEWAY: return True
		d = '' 
		m = tce.RpcMessageReturn(self.inst)
		m.sequence = ctx.msg.sequence
		m.callmsg = ctx.msg
		m.ifidx = ctx.msg.ifidx
		m.call_id = ctx.msg.call_id
		m.conn = ctx.msg.conn
		m.extra = ctx.msg.extra
		if d: m.paramstream += d
		ctx.conn.sendMessage(m)
		return True
	
	
class ITerminalGatewayServerPrx(tce.RpcProxyBase):
	# -- INTERFACE PROXY -- 
	def __init__(self,conn):
		tce.RpcProxyBase.__init__(self)
		self.conn = conn
		self.delta = None
		pass
	
	@staticmethod
	def create(ep,af= tce.AF_WRITE | tce.AF_READ):
		ep.open(af)
		conn = ep.impl
		proxy = ITerminalGatewayServerPrx(conn)
		return proxy
	
	@staticmethod
	def createWithEpName(name):
		ep = tce.RpcCommunicator.instance().currentServer().findEndPointByName(name)
		if not ep: return None
		conn = ep.impl
		proxy = ITerminalGatewayServerPrx(conn)
		return proxy
	
	@staticmethod
	def createWithProxy(prx):
		proxy = ITerminalGatewayServerPrx(prx.conn)
		return proxy
	
	#extra must be map<string,string>
	def ping(self,timeout=None,extra={}):
		# function index: 12
		
		m_1 = tce.RpcMessageCall(self)
		m_1.ifidx = 2
		m_1.opidx = 0
		m_1.extra.setStrDict(extra)
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		r_4 = self.conn.sendMessage(m_1)
		if not r_4:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		if not timeout: timeout = tce.RpcCommunicator.instance().getRpcCallTimeout()
		m_5 = None
		try:
			m_5 = m_1.mtx.get(timeout=timeout)
		except:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_TIMEOUT)
		if m_5.errcode != tce.RpcConsts.RPCERROR_SUCC:
			raise tce.RpcException(m_5.errcode)
		m_1 = m_5
	
	def ping_async(self,async,cookie=None,extra={}):
		# function index: 12
		
		ecode_2 = tce.RpcConsts.RPCERROR_SUCC
		m_1 = tce.RpcMessageCall(self)
		m_1.cookie = cookie
		m_1.ifidx = 2
		m_1.opidx = 0
		m_1.extra.setStrDict(extra)
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		m_1.async = async
		m_1.asyncparser = ITerminalGatewayServerPrx.ping_asyncparser
		r_5 = self.conn.sendMessage(m_1)
		if not r_5:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	@staticmethod
	def ping_asyncparser(m,m2):
		# function index: 12 , m2 - callreturn msg.
		
		stream_1 = m2.paramstream
		user_2 = m.async
		prx_3 = m.prx
		if m2.errcode != tce.RpcConsts.RPCERROR_SUCC: return 
		try:
			idx_4 = 0
			d_5 = stream_1
			r_6 = True
			if r_6:
				user_2(prx_3,m.cookie)
		except:
			traceback.print_exc()
		
	
	def ping_oneway(self,extra={}):
		# function index: idx_4
		
		try:
			m_1 = tce.RpcMessageCall(self)
			m_1.ifidx = 2
			m_1.opidx = 0
			m_1.calltype |= tce.RpcMessage.ONEWAY
			m_1.prx = self
			m_1.conn = m_1.prx.conn
			m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
			m_1.extra.setStrDict(extra)
			r_4 = self.conn.sendMessage(m_1)
			if not r_4:
				raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		except:
			traceback.print_exc()
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	

class IMessageServer(tce.RpcServantBase):
	# -- INTERFACE -- 
	def __init__(self):
		tce.RpcServantBase.__init__(self)
		if not hasattr(self,'delegatecls'):
			self.delegatecls = {}
		self.delegatecls[3] = IMessageServer_delegate
	
	def sendMessage(self,token_list,message,ctx):
		pass
	
	def confirmMessage(self,seqs,ctx):
		pass
	

class IMessageServer_delegate:
	def __init__(self,inst,adapter,conn=None):
		self.index = 3
		self.optlist={}
		self.id = '' 
		self.adapter = adapter
		self.optlist[0] = self.sendMessage
		self.optlist[1] = self.confirmMessage
		
		self.inst = inst
	
	def sendMessage(self,ctx):
		tce.log_debug("callin (sendMessage)")
		d = ctx.msg.paramstream 
		idx = 0
		_p_token_list =[] 
		container = SIDS_t(_p_token_list)
		r,idx = container.unmarshall(d,idx)
		if not r: return False
		_p_message = Message_t()
		r,idx = _p_message.unmarshall(d,idx)
		if not r: return False
		cr = None
		self.inst.sendMessage(_p_token_list,_p_message,ctx)
		if ctx.msg.calltype & tce.RpcMessage.ONEWAY: return True
		d = '' 
		m = tce.RpcMessageReturn(self.inst)
		m.sequence = ctx.msg.sequence
		m.callmsg = ctx.msg
		m.ifidx = ctx.msg.ifidx
		m.call_id = ctx.msg.call_id
		m.conn = ctx.msg.conn
		m.extra = ctx.msg.extra
		if d: m.paramstream += d
		ctx.conn.sendMessage(m)
		return True
	
	def confirmMessage(self,ctx):
		tce.log_debug("callin (confirmMessage)")
		d = ctx.msg.paramstream 
		idx = 0
		_p_seqs =[] 
		container = SIDS_t(_p_seqs)
		r,idx = container.unmarshall(d,idx)
		if not r: return False
		cr = None
		self.inst.confirmMessage(_p_seqs,ctx)
		if ctx.msg.calltype & tce.RpcMessage.ONEWAY: return True
		d = '' 
		m = tce.RpcMessageReturn(self.inst)
		m.sequence = ctx.msg.sequence
		m.callmsg = ctx.msg
		m.ifidx = ctx.msg.ifidx
		m.call_id = ctx.msg.call_id
		m.conn = ctx.msg.conn
		m.extra = ctx.msg.extra
		if d: m.paramstream += d
		ctx.conn.sendMessage(m)
		return True
	
	
class IMessageServerPrx(tce.RpcProxyBase):
	# -- INTERFACE PROXY -- 
	def __init__(self,conn):
		tce.RpcProxyBase.__init__(self)
		self.conn = conn
		self.delta = None
		pass
	
	@staticmethod
	def create(ep,af= tce.AF_WRITE | tce.AF_READ):
		ep.open(af)
		conn = ep.impl
		proxy = IMessageServerPrx(conn)
		return proxy
	
	@staticmethod
	def createWithEpName(name):
		ep = tce.RpcCommunicator.instance().currentServer().findEndPointByName(name)
		if not ep: return None
		conn = ep.impl
		proxy = IMessageServerPrx(conn)
		return proxy
	
	@staticmethod
	def createWithProxy(prx):
		proxy = IMessageServerPrx(prx.conn)
		return proxy
	
	#extra must be map<string,string>
	def sendMessage(self,token_list,message,timeout=None,extra={}):
		# function index: 13
		
		m_1 = tce.RpcMessageCall(self)
		m_1.ifidx = 3
		m_1.opidx = 0
		m_1.extra.setStrDict(extra)
		d_2 = '' 
		container_3 = SIDS_t(token_list)
		d_2 += container_3.marshall()
		m_1.paramstream += d_2
		d_2 = '' 
		d_2 += message.marshall()
		m_1.paramstream += d_2
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		r_4 = self.conn.sendMessage(m_1)
		if not r_4:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		if not timeout: timeout = tce.RpcCommunicator.instance().getRpcCallTimeout()
		m_5 = None
		try:
			m_5 = m_1.mtx.get(timeout=timeout)
		except:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_TIMEOUT)
		if m_5.errcode != tce.RpcConsts.RPCERROR_SUCC:
			raise tce.RpcException(m_5.errcode)
		m_1 = m_5
	
	def sendMessage_async(self,token_list,message,async,cookie=None,extra={}):
		# function index: 13
		
		ecode_2 = tce.RpcConsts.RPCERROR_SUCC
		m_1 = tce.RpcMessageCall(self)
		m_1.cookie = cookie
		m_1.ifidx = 3
		m_1.opidx = 0
		m_1.extra.setStrDict(extra)
		d_3 = '' 
		container_4 = SIDS_t(token_list)
		d_3 += container_4.marshall()
		m_1.paramstream += d_3
		d_3 = '' 
		d_3 += message.marshall()
		m_1.paramstream += d_3
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		m_1.async = async
		m_1.asyncparser = IMessageServerPrx.sendMessage_asyncparser
		r_5 = self.conn.sendMessage(m_1)
		if not r_5:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	@staticmethod
	def sendMessage_asyncparser(m,m2):
		# function index: 13 , m2 - callreturn msg.
		
		stream_1 = m2.paramstream
		user_2 = m.async
		prx_3 = m.prx
		if m2.errcode != tce.RpcConsts.RPCERROR_SUCC: return 
		try:
			idx_4 = 0
			d_5 = stream_1
			r_6 = True
			if r_6:
				user_2(prx_3,m.cookie)
		except:
			traceback.print_exc()
		
	
	def sendMessage_oneway(self,token_list,message,extra={}):
		# function index: idx_4
		
		try:
			m_1 = tce.RpcMessageCall(self)
			m_1.ifidx = 3
			m_1.opidx = 0
			m_1.calltype |= tce.RpcMessage.ONEWAY
			m_1.prx = self
			m_1.conn = m_1.prx.conn
			m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
			m_1.extra.setStrDict(extra)
			d_2 = '' 
			container_3 = SIDS_t(token_list)
			d_2 += container_3.marshall()
			m_1.paramstream += d_2
			d_2 = '' 
			d_2 += message.marshall()
			m_1.paramstream += d_2
			r_4 = self.conn.sendMessage(m_1)
			if not r_4:
				raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		except:
			traceback.print_exc()
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	#extra must be map<string,string>
	def confirmMessage(self,seqs,timeout=None,extra={}):
		# function index: idx_4
		
		m_1 = tce.RpcMessageCall(self)
		m_1.ifidx = 3
		m_1.opidx = 1
		m_1.extra.setStrDict(extra)
		d_2 = '' 
		container_3 = SIDS_t(seqs)
		d_2 += container_3.marshall()
		m_1.paramstream += d_2
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		r_4 = self.conn.sendMessage(m_1)
		if not r_4:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		if not timeout: timeout = tce.RpcCommunicator.instance().getRpcCallTimeout()
		m_5 = None
		try:
			m_5 = m_1.mtx.get(timeout=timeout)
		except:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_TIMEOUT)
		if m_5.errcode != tce.RpcConsts.RPCERROR_SUCC:
			raise tce.RpcException(m_5.errcode)
		m_1 = m_5
	
	def confirmMessage_async(self,seqs,async,cookie=None,extra={}):
		# function index: idx_4
		
		ecode_2 = tce.RpcConsts.RPCERROR_SUCC
		m_1 = tce.RpcMessageCall(self)
		m_1.cookie = cookie
		m_1.ifidx = 3
		m_1.opidx = 1
		m_1.extra.setStrDict(extra)
		d_3 = '' 
		container_4 = SIDS_t(seqs)
		d_3 += container_4.marshall()
		m_1.paramstream += d_3
		m_1.prx = self
		m_1.conn = m_1.prx.conn
		m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
		m_1.async = async
		m_1.asyncparser = IMessageServerPrx.confirmMessage_asyncparser
		r_5 = self.conn.sendMessage(m_1)
		if not r_5:
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	
	@staticmethod
	def confirmMessage_asyncparser(m,m2):
		# function index: idx_4 , m2 - callreturn msg.
		
		stream_1 = m2.paramstream
		user_2 = m.async
		prx_3 = m.prx
		if m2.errcode != tce.RpcConsts.RPCERROR_SUCC: return 
		try:
			idx_4 = 0
			d_5 = stream_1
			r_6 = True
			if r_6:
				user_2(prx_3,m.cookie)
		except:
			traceback.print_exc()
		
	
	def confirmMessage_oneway(self,seqs,extra={}):
		# function index: idx_4
		
		try:
			m_1 = tce.RpcMessageCall(self)
			m_1.ifidx = 3
			m_1.opidx = 1
			m_1.calltype |= tce.RpcMessage.ONEWAY
			m_1.prx = self
			m_1.conn = m_1.prx.conn
			m_1.call_id = tce.RpcCommunicator.instance().currentServer().getId()
			m_1.extra.setStrDict(extra)
			d_2 = '' 
			container_3 = SIDS_t(seqs)
			d_2 += container_3.marshall()
			m_1.paramstream += d_2
			r_4 = self.conn.sendMessage(m_1)
			if not r_4:
				raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
		except:
			traceback.print_exc()
			raise tce.RpcException(tce.RpcConsts.RPCERROR_SENDFAILED)
	

