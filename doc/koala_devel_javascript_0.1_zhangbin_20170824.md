
#Koala消息推送服务 - web开发集成

	v0.1 zhangbin 2017/8/24  created

###1. 简介
-------------
为了实现业务系统投递消息至web前端，业务系统需与Koala系统进行集成。

基本过程:

1. 用户登录业务系统
2. 业务系统携带用户id请求koala系统，获得用户访问令牌token
3. 业务系统将访问令牌token传递到web前端
4. web前端与koala系统进行初始化
5. 接收或者发送系统消息


###2. 依赖程序	
	
	require.js
	tce.js				
	koala.js
	message_client.js
	
###3.定义

####3.1 数据定义

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
    
####3.2 消息接口
	void onMessage(Message_t message);     	接收推送消息入口
	void acknowledget(seq);						发送消息确认接口
	void sendMessage(target,title,content)；	发送消息给指定用户接口
	
###4. 运行过程
详见

	$koala/src/sdk/html5/examples/test_simple.html
	$koala/src/sdk/html5/examples/scripts/main.js

####4.1. 导入模块 
		
	requirejs(['message_client'],function(client){ ... }

####4.2 定义消息入口
	
	function onMessage(message,ctx){
        console.log("message recieved:" + message.content)
        client.acknowledge(message.meta.seq);
    }
    
####4.3 初始化参数
	
	client.open({
    	onMessage: onMessage,					- 消息接收函数
        ping: 5,								- 与服务器长连接保活心跳时间
        mgws_url: 'ws://localhost:14002',		- 接入服务器 uri
        mas_url: 'http://localhost:15555',		- 应用服务器 uri 
        token: token							- 应用服务器用户登录之后传递到前端的访问令牌token
    });
    
####4.4 消息接收和确认
koala接收到服务器推送到达的消息，并将消息传递至 `open`指定的接收函数 `onMessage`，消息对象类型: `Message_t`。 消息接收之后，前端必须调用 `client.acknowledge()`接口，告知消息服务器 消息已被确认，否则当用户再次上线时会再次接收到相同的消息。
	
	function onMessage(message,ctx){
        client.acknowledge(message.meta.seq);   消息接收之后发送确认
    }

####4.5 消息发送 
除了应用系统可以发送消息到前端用户之外，应用web前端也可以给不同用户发送消息。
	
	var target = $('#target').val();
    var title ='标题';
    var content =‘消息正文';
    client.sendMessage(target,title,content);


	


    