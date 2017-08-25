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
import com.sw2us.koala.IUserEventListener;

public class IUserEventListener_delegate extends RpcServantDelegate {
	
	IUserEventListener inst = null;
	public IUserEventListener_delegate(IUserEventListener inst){
		this.ifidx = 1;
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
		return false;
	}	
	
	// func: onUserOnline
	boolean func_0_delegate(RpcMessage m){
		boolean r= false;
		r = false;
		ByteBuffer d = ByteBuffer.wrap(m.paramstream);
		String userid;
		int v_15 = d.getInt();
		byte[] _sb_16 = new byte[v_15];
		d.get(_sb_16);
		userid = new String(_sb_16);
		String gws_id;
		int v_17 = d.getInt();
		byte[] _sb_18 = new byte[v_17];
		d.get(_sb_18);
		gws_id = new String(_sb_18);
		Integer device;
		device = d.getInt();
		IUserEventListener servant = (IUserEventListener)this.inst;
		RpcContext ctx = new RpcContext();
		ctx.msg = m;
		servant.onUserOnline(userid,gws_id,device,ctx);
		if( (m.calltype & tce.RpcMessage.ONEWAY) !=0 ){
			return true;
		}		
		
		return r;
	}	
	
	// func: onUserOffline
	boolean func_1_delegate(RpcMessage m){
		boolean r= false;
		r = false;
		ByteBuffer d = ByteBuffer.wrap(m.paramstream);
		String userid;
		int v_19 = d.getInt();
		byte[] _sb_20 = new byte[v_19];
		d.get(_sb_20);
		userid = new String(_sb_20);
		String gws_id;
		int v_21 = d.getInt();
		byte[] _sb_22 = new byte[v_21];
		d.get(_sb_22);
		gws_id = new String(_sb_22);
		Integer device;
		device = d.getInt();
		IUserEventListener servant = (IUserEventListener)this.inst;
		RpcContext ctx = new RpcContext();
		ctx.msg = m;
		servant.onUserOffline(userid,gws_id,device,ctx);
		if( (m.calltype & tce.RpcMessage.ONEWAY) !=0 ){
			return true;
		}		
		
		return r;
	}	
	
}
