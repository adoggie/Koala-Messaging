/**
 * Created by zhangbin on 11/9/15.
 */

define('pushmessage_client',['tce','koala','jquery'],function(tce,koala,$) {

    P_UNDEFINED = 0;
    P_ANDROID = 1;
    P_IOS = 2;
    P_DESKTOP = 4;
    P_HTML5 = 8;



    function TerminalImpl(app){
        var app = null;
        this.onMessage = function(message,ctx){

        };

        this.onSystemNotification = function(notification,ctx){

        };

        this.onSimpleText = function(text,ctx){
            _on_simple_text(text.title,text.content);
        };

        this.onError = function(errcode,errmsg,ctx){

        };

    }


    TerminalImpl.prototype = new koala.ITerminal();

    var _prx_gws = null;
    var _prx_mexs = null;
    var _access_id = null;
    var _secret_key = null;
    var _token = null;
    var _account = null;
    var _timer_id = null;
    var _server_url =  'ws://localhost:14002';
    var _register_url = 'http://localhost:16001';
    var _ping = 5;

    var _on_simple_text=null;

    // server_url - ws://localhost:14001
    // register_url - http://localhost:16001
    function init( cfg){
        if( cfg ) {
            _server_url = cfg.server_url==undefined?_server_url:cfg.server_url;
            _register_url = cfg.register_url==undefined?_register_url:cfg.register_url;
            _ping = cfg.ping==undefined?_ping:cfg.ping;
            if(cfg.on_simple_text){
                _on_simple_text = cfg.on_simple_text;
            }
        }

        var servant = new TerminalImpl();
        tce.RpcCommunicator.instance().init();
        _prx_gws = koala.ITerminalGatewayServerProxy.create( _server_url );
        _prx_mexs = koala.IMessageServerProxy.createWithProxy(_prx_gws);
        var adapter = tce.RpcCommunicator.instance().createAdapter("message_client");
        adapter.addServant(servant);
        _prx_gws.conn.attachAdapter(adapter);  // 主动接收server推送的消息

    }




    function open(access_id,secret_key,account){
        _access_id = access_id;
        _secret_key = secret_key;
        _account = account;
        register();
        _timer_id = window.setInterval( background_thread, _ping*1000 );
    }

    function background_thread(){
        if(_token == null){
            return;
        }
        register();

        try{
            _prx_gws.ping_oneway();
        }catch(e){
            console.error('ping Gateway server failed:'+ e.toString());
        }
    }

    function close(){
        _token = null;
    }

    function simpleTextAccount(title,content,account,platform){

        var url = _register_url + '/api/push/simple/account/';

        tag  = '';
        $.ajax(
            {
                url: url,
                type: 'POST',
                data: {
                    access_id: _access_id,
                    secret_key: _secret_key,
                    account: account,
                    title: title,
                    content: content,
                    platform: P_UNDEFINED
                },
                dataType: 'json',
                success: function(data){
                    console.log('simpleTextAccount status:'+data.status);
                    if(data.status == 0){
                       ;//
                    }

                },
                error: function(xhr,status,error){
                    console.log( error);
                }

            });
    }

    function register(){
        if( _token!=null){
            return ;
        }
        var url = _register_url + '/api/push/register/';

        device_id = '1123123123123';
        tag  = '';
        $.ajax(
            {
                url: url,
                type: 'POST',
                data: {
                    access_id: _access_id,
                    secret_key: _secret_key,
                    account: _account,
                    device_id: device_id,
                    tag: tag,
                    platform: P_HTML5
                },
                dataType: 'json',
                success: function(data){
                    console.log('register code:'+data.status);
                    if(data.status == 0){
                        _token = data.result;
                        console.log('token:'+_token);
                        _prx_gws.conn.setToken(_token);
                    }

                },
                error: function(xhr,status,error){
                    console.log( error);
                }

            });
    }

    pushmessage_client = {
        init: init,
        open: open,
        close: close,
        simpleTextAccount: simpleTextAccount
    };
    return pushmessage_client;
});

var pushmessage_client = null;
