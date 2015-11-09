
requirejs.config({
    baseUrl: 'scripts',
    paths:{
        //tcelib: 'tce'
        jquery: 'jquery-1.8.3'
    }
});


//var pushmessage_client = null;

//program entry
requirejs(['pushmessage_client'],function(client){

    ACCESS_ID = '0098271772';
    SECRET_KEY = 'qZmthanNk';
    ACCOUNT = '14778920@163.com';
    //DEVICE_ID = 'c2RqZmthanNkZmtsYWpzZGtmbGphc2RmCg==';
    //TAG = 'cute';
    function on_simple_text(title,content,extra){
        console.log("you got :"+title+',content:'+content);
    }

    pushmessage_client.init({
        on_simple_text:  on_simple_text,
        ping: 5,
        server_url: 'ws://localhost:14002',
        register_url: 'http://localhost:16001'
    });

    pushmessage_client.open(ACCESS_ID,SECRET_KEY,ACCOUNT);

    window.setInterval(function(){
        pushmessage_client.simpleTextAccount("test","mamafirst!",ACCOUNT);
    },4*1000);
});