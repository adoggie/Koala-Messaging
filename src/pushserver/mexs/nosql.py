#--coding:utf-8--

import json,traceback,os,time

# from pymongo import MongoClient
from bson.objectid import ObjectId
from desert.misc import currentTimestamp64,hashobject_recursived,hashobject,X,dict_to_python_object
from koala.base import  MessageConfirmValue
from koala.koala_impl import Message_t,SimpleText_t

database = None


def get_collection(cls):
	coll = database[cls.NAME]
	return coll

class BaseType:
	def __init__(self,coll):
		self._id = None
		self.coll_name = coll

	def id(self):
		return self._id

	def getId(self):
		return self.id()

	def save(self):
		d = hashobject(self)
		coll = database[self.coll_name]
		if not self._id:
			_id = coll.insert(d)
			self._id = str(_id)
		else:
			coll.update({'_id':ObjectId(self._id)},d)

	@staticmethod
	def collection(coll_name):
		coll = database[coll_name]
		return coll


class SendMessage(BaseType):
	NAME = 'send_message'
	def __init__(self,message=None):
		BaseType.__init__(self,SendMessage.NAME)
		self.app_id = None
		self.simple_message = True

		self.sender_id = None               #发送者编号
		self.target_id = None           	#接者编号
		self.team_id = None             	#发送到组的消息则要记录组的编号
		self.issue_time = currentTimestamp64()          #邀请发起时间
		self.confirm_time = None                #确认时间
		self.confirm_result = MessageConfirmValue.UNACKED            	#0-未确认;  1 -发送已确认
		self.level = None               			#消息级别 1 – 不可丢弃; 2 – 可丢弃
		self.type = None                           #消息类型

		self.message = None

		self.content = None                        #文本消息
		self.entities = 0            			#消息包含entites的标志 mask
		self.userdata = None


		self.send_time = 0	#发送时间 0 - 即刻发送
		self.expire_time =0 #有效时间 0 - 永久有效
		self.loop_time = 1	#循环发送次数
		self.loop_interval = 0	#循环发送间隔

		self.set_content(message)

	def set_behavior(self,behavior):
		if not behavior:
			return self
		self.send_time = behavior.get('send_time',self.send_time)
		self.expire_time = behavior.get('expire_time',self.expire_time)
		self.loop_time = behavior.get('loop_time',self.loop_time)
		self.loop_interval = behavior.get('loop_interval',self.loop_interval)

		return self


	def set_simple(self,simple=True):
		self.simple_message = simple
		return self

	def set_content(self,message):
		if not message:
			return self
		self.message = message
		self.content = json.dumps( hashobject_recursived(message))
		return self

	def assign(self,r):
		obj = self
		obj.sender_id = r['sender_id']               #发送者编号
		obj.target_id = r['target_id']               #邀请接者编号
		obj.team_id = r['team_id']             #目标地址（邮件或者短信）,send_type非0时有效
		obj.issue_time = r['issue_time']                #邀请文本消息
		obj.confirm_time = r['confirm_time']                 #发送方式 0 - 系统内部邀请； 1 - 短信邀请； 2 - 邮件邀请
		obj.confirm_result = r['confirm_result']             #发送者名称
		obj.level = r['level']              #邀请发起时间
		obj.type = r['type']                #邀请回复时间
		obj.content = r['content']            #接受或者拒绝 0-no_ack ; 1 - accept; 2- reject
		obj.entities = r['entities']
		obj.userdata = r['userdata']
		obj._id = str(r.get('_id'))
		obj.simple_message = r['simple_message']
		obj.app_id = r['app_id']
		return self

	@classmethod
	def get(cls,_id):
		coll = BaseType.collection(cls.NAME)
		obj = None
		try:
			r = coll.find_one({'_id':ObjectId(_id)})
			if not r:
				obj = cls()
				obj.assign(r)
				obj._id = _id
		except:
			obj = None
			traceback.print_exc()
		return obj

	def to_simple(self):
		message = self.to_message()
		text = SimpleText_t()
		text.seq = message.seq
		text.sender_id = message.sender_id
		text.send_time = message.send_time
		text.title = message.title
		text.content = message.content
		return text  # SimpleText_t

	def to_message(self):
		message = Message_t()
		obj = json.loads( self.content)
		dict_to_python_object(obj,message)
		dict_to_python_object(obj['style'],message.style)
		dict_to_python_object(obj['action'],message.action)
		return message # Message_t

	def is_simple(self):
		return self.simple_message


def test():
	class _Dummy:pass
	msg = Message_t()
	# print json.dumps(msg.__dict__)
	print type(msg.action),type(msg.title)
	print type(msg) == type(_Dummy())
	# print hashobject(msg)
	print hashobject_recursived(msg)


if __name__ == '__main__':
	msg = Message_t()
	print type
	# conn = MongoClient()
	# database = conn.test

	# print Notification.collection()

	# n = Notification()
	# n.save()
	# n.sender_id = 'sssssss'
	# n.save()
	# AudioEntity().save()

	# print n.id()
'''
	coll = nosql.get_collection(nosql.Invitation.NAME)
	r = coll.find_one({'_id':ObjectId(seq),'target_id':userid})
'''