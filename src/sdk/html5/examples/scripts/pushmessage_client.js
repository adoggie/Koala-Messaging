/**
 * Created by zhangbin on 11/9/15.
 */

define('pushmessage_client',['tce','koala','jquery'],function(tce,koala,$) {

    P_UNDEFINED = 0
    P_ANDROID = 1
    P_IOS = 2
    P_DESKTOP = 4
    P_HTML5 = 8



        function TerminalImpl(){

            this.onMessage = function(message,ctx){

            };

            this.onSystemNotification = function(notification,ctx){

            };

            this.onSimpleText = function(text,ctx){

            };

            this.onError = function(errcode,errmsg,ctx){

            };

        }


    TerminalImpl.prototype = new koala.ITerminal();

    var prx_gws = null;
    var prx_mexs = null;
    var access_id = null;
    var secret_key = null;
    var token = null;
    var account = null;
    var timer_id = null;
    var server_url = null;
    var register_url = null;

    // server_url - ws://localhost:14001
    // register_url - http://localhost:16001
    function init(server_url,register_url){
        var servant = new TerminalImpl();
        tce.RpcCommunicator.instance().init();
        prx_gws = koala.ITerminalGatewayServerProxy.create( server_url );
        prx_mexs = prx_gws.createWithProxy(prx_gws);
        var adapter = tce.RpcCommunicator.instance().createAdapter("message_client");
        adapter.addServant(servant);
        prx_gws.conn.attachAdapter(adapter);  // 主动接收server推送的消息
    }

    function do_register(){
        if( token != null){
            return ;
        }
    }

    function do_ping(){

    }

    function open(access_id,secret_key,account){

        timer_id = window.setInterval( do_ping, 5 );
    }

    function close(){

    }

    function simpleTextAccount(){

    }

    function register(){
        if( token!=null){
            return ;
        }
        var url = register_url + '/push/register/';

    }





    return {
        init: init,
        open: open,
        close: close,
        simpleTextAccount: simpleTextAccount
    }
});
