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
import com.sw2us.koala.IMessageServer;

public class IMessageServer_delegate extends RpcServantDelegate {
	
	IMessageServer inst = null;
	public IMessageServer_delegate(IMessageServer inst){
		this.ifidx = 3;
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
	
	// func: sendMessage
	boolean func_0_delegate(RpcMessage m){
		boolean r= false;
		r = false;
		ByteBuffer d = ByteBuffer.wrap(m.paramstream);
		Vector<String> token_list = new Vector<String>();
		SIDS_thlp _array_13 = new SIDS_thlp(token_list);
		_array_13.unmarshall(d);
		Message_t message = new Message_t();
		message.unmarshall(d);
		IMessageServer servant = (IMessageServer)this.inst;
		RpcContext ctx = new RpcContext();
		ctx.msg = m;
		servant.sendMessage(token_list,message,ctx);
		if( (m.calltype & tce.RpcMessage.ONEWAY) !=0 ){
			return true;
		}		
		
		return r;
	}	
	
	// func: confirmMessage
	boolean func_1_delegate(RpcMessage m){
		boolean r= false;
		r = false;
		ByteBuffer d = ByteBuffer.wrap(m.paramstream);
		Vector<String> seqs = new Vector<String>();
		SIDS_thlp _array_14 = new SIDS_thlp(seqs);
		_array_14.unmarshall(d);
		IMessageServer servant = (IMessageServer)this.inst;
		RpcContext ctx = new RpcContext();
		ctx.msg = m;
		servant.confirmMessage(seqs,ctx);
		if( (m.calltype & tce.RpcMessage.ONEWAY) !=0 ){
			return true;
		}		
		
		return r;
	}	
	
}
