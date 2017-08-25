

#Koala消息推送系统 － 接口规格定义


Revisions: 	
	

	v0.1 2017/8/25  zhangbin 	    create

##目录


####1.常数定义 

1.1 [错误代码定义](#1.1)


####2.接口定义 

2.1 [获取访问令牌  getTickets ](#2.1)






####3. 测试 
	curl -X PUT/POST/DELETE url 



## 1. 常数定义

<span id="1.1"/>
###1.1 错误代码定义	
    code  	msg 
 	-------------
	0		成功
	1001	参数不完整或数据内容损坏
	1002	目标对象不存在
	1003	无权限操作
	1004    令牌错误
	1005	会话错误
	1006 	用户账号或密码错误
	1007    应用授权错误
	2001    系统内部运行故障
	4001 	消息推送禁止(发送者地址受限)
	4002	未登录或会话过期
	
##2.数据定义
###2.1 Http数据封包
接口调用返回格式： 

	{
	  	status	状态码   0 : succ; others : error  
	  	errcode	错误码
	  	errmsg	错误信息
	  	result	数据内容
	 } 
	 
	 采用json编码(UTF-8)
	 
####2.2 通知消息规格
1. web前端通过与koala服务器建立websocket长连接来实现消息的推送接收。 
2. 前端与koala服务器在网络数据传输时采用二进制封包编码，以Rpc调用方式将接收到的数据解码为分派消息并传递到用户程序中处理。


```

	struct MessageMeta_t{
        string realm;  //
        string seq;     //序号
        string sender;  //
        string stime;   //发送时间
    };
    
    struct Message_t{
        MessageMeta_t meta;
        string title;
        string content;
        Properties_t props;
    };
   
```


## 3. Http接口定义

<span id="3.1"/>
###3.1 获取koala系统访问令牌 
#####名称:

getTickets( app_key , app_secret , user_id ,user_roles)
##### 描述:

每当应用客户登录时到应用系统时，应用系统应向koala系统获取用户访问令牌token，并传递给业务前端，以便后继业务前端访问koala系统时提供凭证。

#####Request
	URL: /koala/api/mas/tickets
	Medthod: POST
	Headers: 
	Character Encoding: utf-8
	Content-Type: x-www-form-urlencoded
	Query Parameters:
	   - app_key 		应用key
	   - secret_key 	应用登录密码
	   - user_id		应用用户标识
	
	   				
#####Response
	Headers:
	Character Encoding: utf-8
	Content-Type: application/json
	Data: 
	  - status	状态码 0 : succ; others : error  
	  - errcode	错误码
	  - errmsg	错误信息
	  - result	登录token
		

#####Examples:

	Request:
	  /koala/api/mas/tickets	
	  app_key=camel&secret_key=EERWERRRRE&user_id=zhangbin
	    
	Response:
	  { 
	    status:0,
	    result: oiwurwurioqweuirqwerjqwewriu==
	  }			
#####Remarks

<span id="3.2"/>
###3.2 消息发送
#####名称:
sendMessage ( ) 
##### 描述:

平台系统或者前端向指定的系统用户发送通知消息。

#####Request
	URL: /koala/api/mas/messages
	Medthod: POST
	Headers: 
	Character Encoding: utf-8
	Content-Type: x-www-form-urlencoded
	Query Parameters:
	  - ticket : access ticket 登录时获取的令牌
	  - users  : 消息接收用户id列表
	  - title  : 消息标题 
	  - content : 消息内容
	  - expire: 消息有效时间 0:永久有效 [可选，默认:0] 
	  - execute: 预定推送时间 0:即刻执行 [可选，默认:0] 

#####Response
	Headers:
	Character Encoding: utf-8
	Content-Type: application/json
	Data: (object) 
	  - status	状态码 0 : succ; others : error  
	  - errcode	错误码
		   
			
#####Examples:

	Request:
	  /koala/api/mas/messages
	  	  
	  tickets=erqewqe12&users=jiangxiaoyu,zhouyang&title="system upgrade"&content="system patching 20:21"
	  	  
	Response:
	  { 
	    status:0,
	  }


	  			
#####Remarks
	
	

<span id="3.3"/>
###3.3 消息确认
#####名称:
acknowledge()
##### 描述:

前端应用接收推送的消息之后，发送确认

#####Request
	URL: /koala/api/mas/messages/ack
	Medthod: POST
	Headers: 
	Character Encoding: utf-8
	Content-Type: multipart/form-data
	Query Parameters:
	  - ticket  	access ticket
	  - sids 	    消息编号列表
	    
		  
#####Response
	Headers:
	Character Encoding: utf-8
	Content-Type: application/json
	Data:(object) 
	  - status
	  - errcode
   
	  			
#####Examples:

	Request:
	  /koala/api/mas/messages/ack
	  
	  tickets=erqewqe12&sids=43233,56772
	  
	Response:
	  { 
	    status:0,
	  }
	  	

#####Remarks
	

## 4. 消息接收

1. 与koala系统集成的业务前端系统，须加入koala的前端sdk，对于javascript须引入`require.js`、`tce.js`、`koala.js`、`message_client.js`

2. js 前端使用 `message_client.open()` 完成与koala服务器的初始化，并提供`onMessage(message,ctx)`接口来实现消息的处理. 
 
#####接收接口
	
	interface ITerminal{
        void onMessage(Message_t message);
    };
    


