/**
 * Created by zhangbin on 11/9/15.
 */

define('message_client',['tce','koala','jquery'],function(tce,koala,$) {

    function TerminalImpl(){

        // Message_t message
        this.onMessage = function(message,ctx){
            if( _onMessage) {
                _onMessage(message, ctx);
            }
;        };

        this.onError = function(errcode,errmsg,ctx){
            if ( _onError ){
                _onError(errcode,errmsg,ctx);
            }
        };

    }


    TerminalImpl.prototype = new koala.ITerminal();

    var _prx_gws    = null;
    var _prx_mexs   = null;
    var _token      = '';
    var _mgws_url   = 'ws://localhost:14002'
    var _mas_url    = 'http://localhost:15555';
    var _ping       = 5;
    var _onMessage  = null;
    var _onError    = null;

    function open( cfg){
        if( cfg ) {
            _mgws_url = cfg.mgws_url;
            _mas_url = cfg.mas_url;
            _ping = cfg.ping;
            _token = cfg.token;

            if(cfg.onMessage){
                _onMessage = cfg.onMessage;
            }
            if(cfg.onError){
                _onError = cfg.onError;
            }
        }

        var servant = new TerminalImpl();
        tce.RpcCommunicator.instance().init();
        _prx_gws = koala.ITerminalGatewayServerProxy.create( _mgws_url );
        _prx_mexs = koala.IMessageServerProxy.createWithProxy(_prx_gws);
        var adapter = tce.RpcCommunicator.instance().createAdapter("message_client");
        adapter.addServant(servant);
        _prx_gws.conn.attachAdapter(adapter);  // 主动接收server推送的消息
        _prx_gws.conn.setToken(_token);

        window.setInterval( do_heartbeat, _ping * 1000 );
    }
    
    function do_heartbeat(){
        try{
            _prx_gws.ping_oneway();
        }catch(e){
            console.error('ping Gateway server failed:'+ e.toString());
        }
    }

    function close(){
        _token = null;
    }

    function _acknowlege(message){
        try{
            _prx_mexs.acknowledge( [message.meta.seq]);
        }catch(e){
            console.error('message acknowledge:'+ e.toString());
        }
    }

    function sendMessage(target,title,content){
        var url = _mas_url + '/koala/api/mas/messages';
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                ticket: _token,
                users: target,
                title: title,
                content: content
            },
            dataType: 'json',
            success: function(data){
                console.log('register code:'+data.status);
                if( data.status !=0){
                    console.log('invoke error:'+data.errmsg);
                }
            },
            error: function(xhr,status,error){
                console.log( error);
            }
        });
    }

    function acknowledge(target){
        var url = _mas_url + '/koala/api/mas/messages/ack';
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                ticket: _token,
                sids: target
            },
            dataType: 'json',
            success: function(data){
                console.log('register code:'+data.status);
            },
            error: function(xhr,status,error){
                console.log( error);
            }
        });
    }

    return {
        open: open,
        close: close,
        acknowledge: acknowledge,
        sendMessage: sendMessage

    };
});

// var message_client = null;
