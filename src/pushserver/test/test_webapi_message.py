#--coding:utf-8--

# 消息发送测试
#



import os,os.path,sys,struct,time,traceback,signal,threading,copy,base64,urllib,json
import datetime,base64
from datetime import datetime



import urllib2,urllib,time

userToken ='AAAAATEAAAAEdGVzdAAAAAAAAAAAU7AjqgAAAAAAAAAAU7Bp+gAAAAUxMTExMQ=='
webserver = 'http://localhost:16001'
webapi = webserver+'/api'

satisfaction={'biz_model':'satisfaction','subtype':5,'time_granule':'day','start_time':1420070400,'end_time':1435708800}


#rt_date': 1420070400, #'2015-01-01', # 1420070400
#                'end_date' : 1435708800, #'2015-07-01', # 1435708800


test_case_list=[
	{'name':'device_register','webapi':'/auth/accessToken/','params':{'user':'wangdazhi','password':'111111','domain':'ylm'}},
	{'name':'simple_device','webapi':'/push/simple/device/',
			'params':{'access_id':'c121e7d470bb11e5ab90ac87a316f916','secret_key':'shahaiNg1y',
				'device_token':'token_001','title':u'Title - simple/device..,','content':u' the blond stand at the corner'
			}
		},
]

case = test_case_list[0]
# res = urllib2.urlopen( webapi + case['webapi'] ,urllib.urlencode(case['params']))
# result = json.loads(res.read())
# print result
# token = result['result']['token']
# print 'auth token:'+token

for case in test_case_list[1:]:
	print 'do test:(',case['name'],')'
	# headers = {
	# 	'SESSION-TOKEN':token,
	# 	'IF-VERSION':'1.0'
	# }
	headers = {}
	opener = urllib2.build_opener()

	if case.get('params'):
		request = urllib2.Request(webapi+case['webapi'],urllib.urlencode(case['params']),headers=headers)
	else:
		request = urllib2.Request(webapi+case['webapi'],headers=headers)
	if case.get('method'):
		request.get_method = lambda:case.get('method')
	print opener.open(request).read()
