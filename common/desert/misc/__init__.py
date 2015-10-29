#-- coding:utf-8 --
from misc import *

class X:
	"""
	从简单数据类型转换成python对象

	p = _x({'name':'boob','body':{'color':'black'},'toys':[1,2,3,],'age':100})
	print p['toys'][1]
	print len(p.toys)
	print p.body.colors
	"""
	def __init__(self,primitive):
		self._data = primitive

	def __getattr__(self, item):
		value = self._data.get(item,None)
		if type(value) in (list,tuple,dict):
			value = X(value)
		return value

	def __len__(self):
		return len(self._data)

	def __str__(self):
		return str(self._data)

	def __getitem__(self, item):
		value = None
		if type(self._data) in (list,tuple):
			value = self._data[item]
			if type(value) in (dict,list,tuple):
				value = X(value)
		elif type(self._data) == dict:
			value = self.__getattr__(item)
		return value


def scope_lock(lock=None):
	pass


def random_password(maxlen=10):
	import string,random
	return ''.join([random.choice(string.digits + string.letters) for i in range(0, maxlen)])

def hashobject_recursived(obj,skip_chars=[]):
	"""
	 	hash python object to json object
	 	example:
	 		class T:
	 			self.color='black'
	 	 	class M:
	 	 		self.name = 'didi'
				self.t = T()

			hashobject_recursived( M() )
			  output:
			     { 'name':'didi','t':{'color':'black'}}
	"""
	class _T:pass

	attrs = [s for  s in dir(obj) if not s.startswith('__') and  s not in skip_chars ]
	kvs={}
	for k in attrs:
		attr = getattr(obj, k)
		if  callable(attr): # excluded function
			continue
		elif type( attr) == type(_T()):
			kvs[k] = hashobject_recursived( attr,skip_chars )
		else:
			kvs[k] = attr
	return kvs