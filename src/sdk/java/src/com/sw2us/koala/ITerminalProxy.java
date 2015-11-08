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


public class ITerminalProxy extends RpcProxyBase{
	//# -- INTERFACE PROXY -- 
	
	public ITerminalProxy(RpcConnection conn){
		this.conn = conn;
	}	
	
	public static ITerminalProxy create(String host,int port,Boolean ssl_enable){
		int type = RpcConsts.CONNECTION_SOCK;
		if (ssl_enable) type |= RpcConsts.CONNECTION_SSL;
		RpcConnection conn = RpcCommunicator.instance().createConnection(type,host,port);
		ITerminalProxy prx = new ITerminalProxy(conn);
		return prx;
	}	
	public static ITerminalProxy createWithProxy(RpcProxyBase proxy){
		ITerminalProxy prx = new ITerminalProxy(proxy.conn);
		return prx;
	}	
	
	public void destroy(){
		try{
			conn.close();
		}catch(Exception e){
			RpcCommunicator.instance().getLogger().error(e.getMessage());
		}		
	}	
	
	public void onSimpleText(SimpleText_t text) throws RpcException{
onSimpleText(text,tce.RpcCommunicator.instance().getProperty_DefaultCallWaitTime(),null);		
	}	
	// timeout - msec ,  0 means waiting infinitely
	public void onSimpleText(SimpleText_t text,int timeout,HashMap<String,String> props) throws RpcException{
		boolean r_1 = false;
		RpcMessage m_2 = new RpcMessage(RpcMessage.CALL);
		m_2.ifidx = 0;
		m_2.opidx = 0;
		m_2.paramsize = 1;
		m_2.extra.setProperties(props);
		try{
			ByteArrayOutputStream bos_3 = new ByteArrayOutputStream();
			DataOutputStream dos_4 = new DataOutputStream(bos_3);
			text.marshall(dos_4);
			m_2.paramstream = bos_3.toByteArray();
			m_2.prx = this;
		}catch(Exception e){
			throw new RpcException(RpcConsts.RPCERROR_DATADIRTY,e.toString());
		}		
		synchronized(m_2){
			r_1 = this.conn.sendMessage(m_2);
			if(!r_1){
				throw new RpcException(RpcConsts.RPCERROR_SENDFAILED);
			}			
			try{
				if( timeout > 0) m_2.wait(timeout);
				else m_2.wait();
			}catch(Exception e){
				throw new RpcException(RpcConsts.RPCERROR_INTERNAL_EXCEPTION,e.getMessage());
			}			
		}		
		if (m_2.errcode != RpcConsts.RPCERROR_SUCC){
			throw new RpcException(m_2.errcode);
		}		
		if( m_2.result == null){
			throw new RpcException(RpcConsts.RPCERROR_TIMEOUT);
		}		
	}	
	
	public void onSimpleText_oneway(SimpleText_t text,HashMap<String,String> props) throws RpcException{
		boolean r_1 = false;
		RpcMessage m_2 = new RpcMessage(RpcMessage.CALL|RpcMessage.ONEWAY);
		m_2.ifidx = 0;
		m_2.opidx = 0;
		m_2.paramsize = 1;
		m_2.extra.setProperties(props);
		try{
			ByteArrayOutputStream bos_3 = new ByteArrayOutputStream();
			DataOutputStream dos_4 = new DataOutputStream(bos_3);
			text.marshall(dos_4);
			m_2.paramstream = bos_3.toByteArray();
			m_2.prx = this;
		}catch(Exception e){
			throw new RpcException(RpcConsts.RPCERROR_DATADIRTY,e.toString());
		}		
		r_1 = this.conn.sendMessage(m_2);
		if(!r_1){
			throw new RpcException(RpcConsts.RPCERROR_SENDFAILED);
		}		
	}	
	
	public void onSimpleText_async(SimpleText_t text,ITerminal_AsyncCallBack async,HashMap<String,String> props) throws RpcException{
		onSimpleText_async(text,async,props,null);
	}	
	
	public void onSimpleText_async(SimpleText_t text,ITerminal_AsyncCallBack async) throws RpcException{
		onSimpleText_async(text,async,null,null);
	}	
	
	public void onSimpleText_async(SimpleText_t text,ITerminal_AsyncCallBack async,HashMap<String,String> props,Object cookie) throws RpcException{
		boolean r_5 = false;
		RpcMessage m_6 = new RpcMessage(RpcMessage.CALL|RpcMessage.ASYNC);
		m_6.ifidx = 0;
		m_6.opidx = 0;
		m_6.paramsize = 1;
		m_6.extra.setProperties(props);
		m_6.cookie = cookie;
		try{
			ByteArrayOutputStream bos_7 = new ByteArrayOutputStream();
			DataOutputStream dos_8 = new DataOutputStream(bos_7);
			text.marshall(dos_8);
			m_6.paramstream = bos_7.toByteArray();
			m_6.prx = this;
			m_6.async = async;
		}catch(Exception e){
			throw new RpcException(RpcConsts.RPCERROR_DATADIRTY,e.toString());
		}		
		r_5 = this.conn.sendMessage(m_6);
		if(!r_5){
			throw new RpcException(RpcConsts.RPCERROR_SENDFAILED);
		}		
	}	
	
	
	
	public void onMessage(Message_t message) throws RpcException{
onMessage(message,tce.RpcCommunicator.instance().getProperty_DefaultCallWaitTime(),null);		
	}	
	// timeout - msec ,  0 means waiting infinitely
	public void onMessage(Message_t message,int timeout,HashMap<String,String> props) throws RpcException{
		boolean r_1 = false;
		RpcMessage m_2 = new RpcMessage(RpcMessage.CALL);
		m_2.ifidx = 0;
		m_2.opidx = 1;
		m_2.paramsize = 1;
		m_2.extra.setProperties(props);
		try{
			ByteArrayOutputStream bos_3 = new ByteArrayOutputStream();
			DataOutputStream dos_4 = new DataOutputStream(bos_3);
			message.marshall(dos_4);
			m_2.paramstream = bos_3.toByteArray();
			m_2.prx = this;
		}catch(Exception e){
			throw new RpcException(RpcConsts.RPCERROR_DATADIRTY,e.toString());
		}		
		synchronized(m_2){
			r_1 = this.conn.sendMessage(m_2);
			if(!r_1){
				throw new RpcException(RpcConsts.RPCERROR_SENDFAILED);
			}			
			try{
				if( timeout > 0) m_2.wait(timeout);
				else m_2.wait();
			}catch(Exception e){
				throw new RpcException(RpcConsts.RPCERROR_INTERNAL_EXCEPTION,e.getMessage());
			}			
		}		
		if (m_2.errcode != RpcConsts.RPCERROR_SUCC){
			throw new RpcException(m_2.errcode);
		}		
		if( m_2.result == null){
			throw new RpcException(RpcConsts.RPCERROR_TIMEOUT);
		}		
	}	
	
	public void onMessage_oneway(Message_t message,HashMap<String,String> props) throws RpcException{
		boolean r_1 = false;
		RpcMessage m_2 = new RpcMessage(RpcMessage.CALL|RpcMessage.ONEWAY);
		m_2.ifidx = 0;
		m_2.opidx = 1;
		m_2.paramsize = 1;
		m_2.extra.setProperties(props);
		try{
			ByteArrayOutputStream bos_3 = new ByteArrayOutputStream();
			DataOutputStream dos_4 = new DataOutputStream(bos_3);
			message.marshall(dos_4);
			m_2.paramstream = bos_3.toByteArray();
			m_2.prx = this;
		}catch(Exception e){
			throw new RpcException(RpcConsts.RPCERROR_DATADIRTY,e.toString());
		}		
		r_1 = this.conn.sendMessage(m_2);
		if(!r_1){
			throw new RpcException(RpcConsts.RPCERROR_SENDFAILED);
		}		
	}	
	
	public void onMessage_async(Message_t message,ITerminal_AsyncCallBack async,HashMap<String,String> props) throws RpcException{
		onMessage_async(message,async,props,null);
	}	
	
	public void onMessage_async(Message_t message,ITerminal_AsyncCallBack async) throws RpcException{
		onMessage_async(message,async,null,null);
	}	
	
	public void onMessage_async(Message_t message,ITerminal_AsyncCallBack async,HashMap<String,String> props,Object cookie) throws RpcException{
		boolean r_5 = false;
		RpcMessage m_6 = new RpcMessage(RpcMessage.CALL|RpcMessage.ASYNC);
		m_6.ifidx = 0;
		m_6.opidx = 1;
		m_6.paramsize = 1;
		m_6.extra.setProperties(props);
		m_6.cookie = cookie;
		try{
			ByteArrayOutputStream bos_7 = new ByteArrayOutputStream();
			DataOutputStream dos_8 = new DataOutputStream(bos_7);
			message.marshall(dos_8);
			m_6.paramstream = bos_7.toByteArray();
			m_6.prx = this;
			m_6.async = async;
		}catch(Exception e){
			throw new RpcException(RpcConsts.RPCERROR_DATADIRTY,e.toString());
		}		
		r_5 = this.conn.sendMessage(m_6);
		if(!r_5){
			throw new RpcException(RpcConsts.RPCERROR_SENDFAILED);
		}		
	}	
	
	
	
	public void onError(String errcode,String errmsg) throws RpcException{
onError(errcode,errmsg,tce.RpcCommunicator.instance().getProperty_DefaultCallWaitTime(),null);		
	}	
	// timeout - msec ,  0 means waiting infinitely
	public void onError(String errcode,String errmsg,int timeout,HashMap<String,String> props) throws RpcException{
		boolean r_1 = false;
		RpcMessage m_2 = new RpcMessage(RpcMessage.CALL);
		m_2.ifidx = 0;
		m_2.opidx = 2;
		m_2.paramsize = 2;
		m_2.extra.setProperties(props);
		try{
			ByteArrayOutputStream bos_3 = new ByteArrayOutputStream();
			DataOutputStream dos_4 = new DataOutputStream(bos_3);
			byte[] sb_5 = errcode.getBytes();
			dos_4.writeInt(sb_5.length);
			dos_4.write(sb_5,0,sb_5.length);
			byte[] sb_6 = errmsg.getBytes();
			dos_4.writeInt(sb_6.length);
			dos_4.write(sb_6,0,sb_6.length);
			m_2.paramstream = bos_3.toByteArray();
			m_2.prx = this;
		}catch(Exception e){
			throw new RpcException(RpcConsts.RPCERROR_DATADIRTY,e.toString());
		}		
		synchronized(m_2){
			r_1 = this.conn.sendMessage(m_2);
			if(!r_1){
				throw new RpcException(RpcConsts.RPCERROR_SENDFAILED);
			}			
			try{
				if( timeout > 0) m_2.wait(timeout);
				else m_2.wait();
			}catch(Exception e){
				throw new RpcException(RpcConsts.RPCERROR_INTERNAL_EXCEPTION,e.getMessage());
			}			
		}		
		if (m_2.errcode != RpcConsts.RPCERROR_SUCC){
			throw new RpcException(m_2.errcode);
		}		
		if( m_2.result == null){
			throw new RpcException(RpcConsts.RPCERROR_TIMEOUT);
		}		
	}	
	
	public void onError_oneway(String errcode,String errmsg,HashMap<String,String> props) throws RpcException{
		boolean r_1 = false;
		RpcMessage m_2 = new RpcMessage(RpcMessage.CALL|RpcMessage.ONEWAY);
		m_2.ifidx = 0;
		m_2.opidx = 2;
		m_2.paramsize = 2;
		m_2.extra.setProperties(props);
		try{
			ByteArrayOutputStream bos_3 = new ByteArrayOutputStream();
			DataOutputStream dos_4 = new DataOutputStream(bos_3);
			byte[] sb_5 = errcode.getBytes();
			dos_4.writeInt(sb_5.length);
			dos_4.write(sb_5,0,sb_5.length);
			byte[] sb_6 = errmsg.getBytes();
			dos_4.writeInt(sb_6.length);
			dos_4.write(sb_6,0,sb_6.length);
			m_2.paramstream = bos_3.toByteArray();
			m_2.prx = this;
		}catch(Exception e){
			throw new RpcException(RpcConsts.RPCERROR_DATADIRTY,e.toString());
		}		
		r_1 = this.conn.sendMessage(m_2);
		if(!r_1){
			throw new RpcException(RpcConsts.RPCERROR_SENDFAILED);
		}		
	}	
	
	public void onError_async(String errcode,String errmsg,ITerminal_AsyncCallBack async,HashMap<String,String> props) throws RpcException{
		onError_async(errcode,errmsg,async,props,null);
	}	
	
	public void onError_async(String errcode,String errmsg,ITerminal_AsyncCallBack async) throws RpcException{
		onError_async(errcode,errmsg,async,null,null);
	}	
	
	public void onError_async(String errcode,String errmsg,ITerminal_AsyncCallBack async,HashMap<String,String> props,Object cookie) throws RpcException{
		boolean r_7 = false;
		RpcMessage m_8 = new RpcMessage(RpcMessage.CALL|RpcMessage.ASYNC);
		m_8.ifidx = 0;
		m_8.opidx = 2;
		m_8.paramsize = 2;
		m_8.extra.setProperties(props);
		m_8.cookie = cookie;
		try{
			ByteArrayOutputStream bos_9 = new ByteArrayOutputStream();
			DataOutputStream dos_10 = new DataOutputStream(bos_9);
			byte[] sb_11 = errcode.getBytes();
			dos_10.writeInt(sb_11.length);
			dos_10.write(sb_11,0,sb_11.length);
			byte[] sb_12 = errmsg.getBytes();
			dos_10.writeInt(sb_12.length);
			dos_10.write(sb_12,0,sb_12.length);
			m_8.paramstream = bos_9.toByteArray();
			m_8.prx = this;
			m_8.async = async;
		}catch(Exception e){
			throw new RpcException(RpcConsts.RPCERROR_DATADIRTY,e.toString());
		}		
		r_7 = this.conn.sendMessage(m_8);
		if(!r_7){
			throw new RpcException(RpcConsts.RPCERROR_SENDFAILED);
		}		
	}	
	
	
	
	public void onSystemNotification(Notification_t notification) throws RpcException{
onSystemNotification(notification,tce.RpcCommunicator.instance().getProperty_DefaultCallWaitTime(),null);		
	}	
	// timeout - msec ,  0 means waiting infinitely
	public void onSystemNotification(Notification_t notification,int timeout,HashMap<String,String> props) throws RpcException{
		boolean r_1 = false;
		RpcMessage m_2 = new RpcMessage(RpcMessage.CALL);
		m_2.ifidx = 0;
		m_2.opidx = 3;
		m_2.paramsize = 1;
		m_2.extra.setProperties(props);
		try{
			ByteArrayOutputStream bos_3 = new ByteArrayOutputStream();
			DataOutputStream dos_4 = new DataOutputStream(bos_3);
			notification.marshall(dos_4);
			m_2.paramstream = bos_3.toByteArray();
			m_2.prx = this;
		}catch(Exception e){
			throw new RpcException(RpcConsts.RPCERROR_DATADIRTY,e.toString());
		}		
		synchronized(m_2){
			r_1 = this.conn.sendMessage(m_2);
			if(!r_1){
				throw new RpcException(RpcConsts.RPCERROR_SENDFAILED);
			}			
			try{
				if( timeout > 0) m_2.wait(timeout);
				else m_2.wait();
			}catch(Exception e){
				throw new RpcException(RpcConsts.RPCERROR_INTERNAL_EXCEPTION,e.getMessage());
			}			
		}		
		if (m_2.errcode != RpcConsts.RPCERROR_SUCC){
			throw new RpcException(m_2.errcode);
		}		
		if( m_2.result == null){
			throw new RpcException(RpcConsts.RPCERROR_TIMEOUT);
		}		
	}	
	
	public void onSystemNotification_oneway(Notification_t notification,HashMap<String,String> props) throws RpcException{
		boolean r_1 = false;
		RpcMessage m_2 = new RpcMessage(RpcMessage.CALL|RpcMessage.ONEWAY);
		m_2.ifidx = 0;
		m_2.opidx = 3;
		m_2.paramsize = 1;
		m_2.extra.setProperties(props);
		try{
			ByteArrayOutputStream bos_3 = new ByteArrayOutputStream();
			DataOutputStream dos_4 = new DataOutputStream(bos_3);
			notification.marshall(dos_4);
			m_2.paramstream = bos_3.toByteArray();
			m_2.prx = this;
		}catch(Exception e){
			throw new RpcException(RpcConsts.RPCERROR_DATADIRTY,e.toString());
		}		
		r_1 = this.conn.sendMessage(m_2);
		if(!r_1){
			throw new RpcException(RpcConsts.RPCERROR_SENDFAILED);
		}		
	}	
	
	public void onSystemNotification_async(Notification_t notification,ITerminal_AsyncCallBack async,HashMap<String,String> props) throws RpcException{
		onSystemNotification_async(notification,async,props,null);
	}	
	
	public void onSystemNotification_async(Notification_t notification,ITerminal_AsyncCallBack async) throws RpcException{
		onSystemNotification_async(notification,async,null,null);
	}	
	
	public void onSystemNotification_async(Notification_t notification,ITerminal_AsyncCallBack async,HashMap<String,String> props,Object cookie) throws RpcException{
		boolean r_5 = false;
		RpcMessage m_6 = new RpcMessage(RpcMessage.CALL|RpcMessage.ASYNC);
		m_6.ifidx = 0;
		m_6.opidx = 3;
		m_6.paramsize = 1;
		m_6.extra.setProperties(props);
		m_6.cookie = cookie;
		try{
			ByteArrayOutputStream bos_7 = new ByteArrayOutputStream();
			DataOutputStream dos_8 = new DataOutputStream(bos_7);
			notification.marshall(dos_8);
			m_6.paramstream = bos_7.toByteArray();
			m_6.prx = this;
			m_6.async = async;
		}catch(Exception e){
			throw new RpcException(RpcConsts.RPCERROR_DATADIRTY,e.toString());
		}		
		r_5 = this.conn.sendMessage(m_6);
		if(!r_5){
			throw new RpcException(RpcConsts.RPCERROR_SENDFAILED);
		}		
	}	
	
	
}
