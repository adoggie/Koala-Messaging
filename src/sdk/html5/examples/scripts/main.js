
requirejs.config({
    baseUrl: 'scripts',
    paths:{
        //tcelib: 'tce'
        jquery: 'jquery-1.8.3'
    }
});

//program entry
requirejs(['tce','koala','jquery'],function(tce,koala,$){


function TerminalImpl(){
    this.onMessage = function(message,ctx){
        debug_info('ITerminal::onMessage:' + message);
    };
}

TerminalImpl.prototype = new koala.ITerminal();
var servant = new TerminalImpl();
tce.RpcCommunicator.instance().init();
var prxServer = ServerProxy.create('ws://localhost:14001');
var adapter = tce.RpcCommunicator.instance().createAdapter("test");
adapter.addServant(servant);
prxServer.conn.attachAdapter(adapter);  // 主动接收server推送的消息


    console.log( typeof tce.RpcCommunicator);
    console.log(koala.ITerminal);
    console.log('aaaa');
});