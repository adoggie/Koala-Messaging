package com.sw2us.koala.client;


//import com.sw2us.koala.ITerminal;

import com.sw2us.koala.ITerminal;
import com.sw2us.koala.Message_t;
import com.sw2us.koala.Notification_t;
import com.sw2us.koala.SimpleText_t;
import tce.RpcContext;

import java.util.HashMap;

/**
 * Created by scott on 11/7/15.
 */
class TerminalImpl extends ITerminal {
	PushMessageClient _client;

	public TerminalImpl( PushMessageClient client){
		_client = client;
	}

	@Override
	public void onSimpleText(SimpleText_t text, RpcContext ctx) {
		super.onSimpleText(text, ctx);
//		_client.onSimpleText(text.title,text.content,new HashMap<String,String>());
		_client.onSimpleText(text);

	}

	@Override
	public void onMessage(Message_t message, RpcContext ctx) {
		super.onMessage(message, ctx);
	}

	@Override
	public void onError(String errcode, String errmsg, RpcContext ctx) {
		super.onError(errcode, errmsg, ctx);
	}

	@Override
	public void onSystemNotification(Notification_t notification, RpcContext ctx) {
		super.onSystemNotification(notification, ctx);
	}
}
