package com.sw2us.koala;

//import tce.*;
//import javax.xml.parsers.*;
//import org.w3c.dom.*;
//import java.io.*;
//import java.nio.*;
//import java.util.*;
	
import tce.*;
import java.io.*;
import java.nio.*;
import java.util.*;
import com.sw2us.koala.ITerminal;

public class ITerminal_delegate extends RpcServantDelegate {
	
	ITerminal inst = null;
	public ITerminal_delegate(ITerminal inst){
		this.ifidx = 0;
		this.inst = inst;
	}	
	
	@Override
	public boolean invoke(RpcMessage m){
		if(m.opidx == 0 ){
			return func_0_delegate(m);
		}		
		if(m.opidx == 1 ){
			return func_1_delegate(m);
		}		
		if(m.opidx == 2 ){
			return func_2_delegate(m);
		}		
		if(m.opidx == 3 ){
			return func_3_delegate(m);
		}		
		return false;
	}	
	
	// func: onSimpleText
	boolean func_0_delegate(RpcMessage m){
		boolean r= false;
		r = false;
		ByteBuffer d = ByteBuffer.wrap(m.paramstream);
		SimpleText_t text = new SimpleText_t();
		text.unmarshall(d);
		ITerminal servant = (ITerminal)this.inst;
		RpcContext ctx = new RpcContext();
		ctx.msg = m;
		servant.onSimpleText(text,ctx);
		if( (m.calltype & tce.RpcMessage.ONEWAY) !=0 ){
			return true;
		}		
		
		return r;
	}	
	
	// func: onMessage
	boolean func_1_delegate(RpcMessage m){
		boolean r= false;
		r = false;
		ByteBuffer d = ByteBuffer.wrap(m.paramstream);
		Message_t message = new Message_t();
		message.unmarshall(d);
		ITerminal servant = (ITerminal)this.inst;
		RpcContext ctx = new RpcContext();
		ctx.msg = m;
		servant.onMessage(message,ctx);
		if( (m.calltype & tce.RpcMessage.ONEWAY) !=0 ){
			return true;
		}		
		
		return r;
	}	
	
	// func: onError
	boolean func_2_delegate(RpcMessage m){
		boolean r= false;
		r = false;
		ByteBuffer d = ByteBuffer.wrap(m.paramstream);
		String errcode;
		int v_13 = d.getInt();
		byte[] _sb_14 = new byte[v_13];
		d.get(_sb_14);
		errcode = new String(_sb_14);
		String errmsg;
		int v_15 = d.getInt();
		byte[] _sb_16 = new byte[v_15];
		d.get(_sb_16);
		errmsg = new String(_sb_16);
		ITerminal servant = (ITerminal)this.inst;
		RpcContext ctx = new RpcContext();
		ctx.msg = m;
		servant.onError(errcode,errmsg,ctx);
		if( (m.calltype & tce.RpcMessage.ONEWAY) !=0 ){
			return true;
		}		
		
		return r;
	}	
	
	// func: onSystemNotification
	boolean func_3_delegate(RpcMessage m){
		boolean r= false;
		r = false;
		ByteBuffer d = ByteBuffer.wrap(m.paramstream);
		Notification_t notification = new Notification_t();
		notification.unmarshall(d);
		ITerminal servant = (ITerminal)this.inst;
		RpcContext ctx = new RpcContext();
		ctx.msg = m;
		servant.onSystemNotification(notification,ctx);
		if( (m.calltype & tce.RpcMessage.ONEWAY) !=0 ){
			return true;
		}		
		
		return r;
	}	
	
}
