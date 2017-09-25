
requirejs.config({
    baseUrl: 'scripts',
    paths:{
        jquery: 'jquery-1.8.3'
    }
});


requirejs(['message_client'],function(client){

    $(document).ready(function() {
        $('#btnLogin').click(function(e){
            login();
        });

        $('#btnSend').click(function(e){

            var target = $('#target').val();
            var title ='测试标题';
            var content =$('#content').val();
            client.sendMessage(target,title,content);
        });
    });


    /*
     login()
     模拟业务服务器登陆消息系统,提供 app_id,secret_key,user_id ,返回访问消息服务的令牌 token
     */
    function login(){
        // var url = "http://localhost:15555" + '/koala/api/mas/tickets';
        var url = "http://192.168.1.233:15555" + '/koala/api/mas/tickets';
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                app_id: $('#app_id').val(),
                secret_key: $('#secret_key').val(),
                user_id: $('#user').val(),
            },
            dataType: 'json',
            success: function(data){
                $('#message').text(data.result);
                afterLogin(data.result);
            },
            error: function(xhr,status,error){
                console.log( error);
            }
        });
    }


    //var token ="eyJyZWFsbSI6ICJjYW1lbCIsICJhcHBfaWQiOiAiY2FtZWwiLCAiY3JlYXRlX3RpbWUiOiAxNTAyNTUyNDk3LCAidGltZSI6IDE1MDI1NTI1MTksICJleHBpcmVfdGltZSI6IDE1MDM0MTY0OTcsICJ1c2VyX2lkIjogImFkbWluIn0=";

    function onMessage(message,ctx){
        console.log("message recieved:"+message.content)
        $('#message').text('seq:'+message.meta.seq + ' title:'+ message.title + ' content:'+message.content);
        client.acknowledge(message.meta.seq);
    }

    function afterLogin(token) {

        client.open({
            onMessage: onMessage,
            ping: 5,
            // mgws_url: 'ws://localhost:14002',
            mgws_url: 'ws://192.168.1.233:8888/mexs/',
            // mas_url: 'http://localhost:15555',
            mas_url: 'http://192.168.1.233:8888/',
            token: token
        });

        window.setInterval(function () {
            console.log("i am a timer!");
        }, 4 * 1000);

    }
});
