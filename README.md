# koala - 消息推送系统

### 1. 系统介绍 

在移动互联网应用场景中，用户与系统、子系统之间都会产生大量的消息交互，这些交互消息包括实时消息、非实时消息、业务消息、系统消息等等。 

koala服务提供独立的消息推送服务，第三方应用系统通过koala提供的服务可实现：

	1. 平台系统推送消息到前端移动app的功能
	2. 移动app之间消息的互推

### 2.系统结构

### 2.1 接入服务 MGWS 
(Message Gateway Service)


### 2.2 应用服务 MAS 
(Message Application Service) 

### 2.3 消息交换服务 MEXS 
(Message Exchange Service)

## 3. 系统设计 
1.[koala消息推送服务系统设计](https://github.com/adoggie/Koala-Messaging/blob/master/doc/Koala%E6%B6%88%E6%81%AF%E6%8E%A8%E9%80%81%E6%9C%8D%E5%8A%A1%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A1.pdf)

2.[webapi接口设计](https://github.com/adoggie/Koala-Messaging/blob/master/doc/koala_webapi_0.1_zhangbin_20170824.md)

3.[javascript集成](https://github.com/adoggie/Koala-Messaging/blob/master/doc/koala_devel_javascript_0.1_zhangbin_20170824.md)

## 4. exmaples

[javascript](https://github.com/adoggie/Koala-Messaging/tree/master/src/sdk/html5/examples)

## 99. 工程目录
    
    koala_messaging/
    ├── ChangeLog.md
    ├── INSTALL.md
    ├── README.md
    ├── RELEASE.md
    ├── data
    ├── design
    ├── etc
    │   ├── config.yaml
    │   ├── server_eps.conf
    │   ├── services.xml
    │   ├── settings_mas.yaml
    │   ├── settings_mexs.yaml
    │   └── settings_mgws.yaml
    ├── logs
    ├── run
    │   ├── start-server-mas.sh
    │   ├── start-server-mexs.sh
    │   ├── start-server-mgws.sh
    ├── scripts
    │   └── dist_linux_dev.sh
    └── src
        ├── mas
        ├── mexs
        ├── mgws
        ├── requirements.txt
        ├── sdk
        ├── server.py
        ├── tests
    
    
