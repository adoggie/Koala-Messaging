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


public class IMessageServerProxy extends RpcProxyBase{
	//# -- INTERFACE PROXY -- 
	
	public IMessageServerProxy(RpcConnection conn){
		this.conn = conn;
	}	
	
	public static IMessageServerProxy create(String host,int port,Boolean ssl_enable){
		int type = RpcConsts.CONNECTION_SOCK;
		if (ssl_enable) type |= RpcConsts.CONNECTION_SSL;
		RpcConnection conn = RpcCommunicator.instance().createConnection(type,host,port);
		IMessageServerProxy prx = new IMessageServerProxy(conn);
		return prx;
	}	
	public static IMessageServerProxy createWithProxy(RpcProxyBase proxy){
		IMessageServerProxy prx = new IMessageServerProxy(proxy.conn);
		return prx;
	}	
	
	public void destroy(){
		try{
			conn.close();
		}catch(Exception e){
			RpcCommunicator.instance().getLogger().error(e.getMessage());
		}		
	}	
	
	public void sendMessage(Vector<String> token_list,Message_t message) throws RpcException{
sendMessage(token_list,message,tce.RpcCommunicator.instance().getProperty_DefaultCallWaitTime(),null);		
	}	
	// timeout - msec ,  0 means waiting infinitely
	public void sendMessage(Vector<String> token_list,Message_t message,int timeout,HashMap<String,String> props) throws RpcException{
		boolean r_1 = false;
		RpcMessage m_2 = new RpcMessage(RpcMessage.CALL);
		m_2.ifidx = 3;
		m_2.opidx = 0;
		m_2.paramsize = 2;
		m_2.extra.setProperties(props);
		try{
			ByteArrayOutputStream bos_3 = new ByteArrayOutputStream();
			DataOutputStream dos_4 = new DataOutputStream(bos_3);
			SIDS_thlp c_5 = new SIDS_thlp(token_list);
			c_5.marshall(dos_4);
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
	
	public void sendMessage_oneway(Vector<String> token_list,Message_t message,HashMap<String,String> props) throws RpcException{
		boolean r_1 = false;
		RpcMessage m_2 = new RpcMessage(RpcMessage.CALL|RpcMessage.ONEWAY);
		m_2.ifidx = 3;
		m_2.opidx = 0;
		m_2.paramsize = 2;
		m_2.extra.setProperties(props);
		try{
			ByteArrayOutputStream bos_3 = new ByteArrayOutputStream();
			DataOutputStream dos_4 = new DataOutputStream(bos_3);
			SIDS_thlp c_5 = new SIDS_thlp(token_list);
			c_5.marshall(dos_4);
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
	
	public void sendMessage_async(Vector<String> token_list,Message_t message,IMessageServer_AsyncCallBack async,HashMap<String,String> props) throws RpcException{
		sendMessage_async(token_list,message,async,props,null);
	}	
	
	public void sendMessage_async(Vector<String> token_list,Message_t message,IMessageServer_AsyncCallBack async) throws RpcException{
		sendMessage_async(token_list,message,async,null,null);
	}	
	
	public void sendMessage_async(Vector<String> token_list,Message_t message,IMessageServer_AsyncCallBack async,HashMap<String,String> props,Object cookie) throws RpcException{
		boolean r_6 = false;
		RpcMessage m_7 = new RpcMessage(RpcMessage.CALL|RpcMessage.ASYNC);
		m_7.ifidx = 3;
		m_7.opidx = 0;
		m_7.paramsize = 2;
		m_7.extra.setProperties(props);
		m_7.cookie = cookie;
		try{
			ByteArrayOutputStream bos_8 = new ByteArrayOutputStream();
			DataOutputStream dos_9 = new DataOutputStream(bos_8);
			SIDS_thlp c_10 = new SIDS_thlp(token_list);
			c_10.marshall(dos_9);
			message.marshall(dos_9);
			m_7.paramstream = bos_8.toByteArray();
			m_7.prx = this;
			m_7.async = async;
		}catch(Exception e){
			throw new RpcException(RpcConsts.RPCERROR_DATADIRTY,e.toString());
		}		
		r_6 = this.conn.sendMessage(m_7);
		if(!r_6){
			throw new RpcException(RpcConsts.RPCERROR_SENDFAILED);
		}		
	}	
	
	
	
	public void confirmMessage(Vector<String> seqs) throws RpcException{
confirmMessage(seqs,tce.RpcCommunicator.instance().getProperty_DefaultCallWaitTime(),null);		
	}	
	// timeout - msec ,  0 means waiting infinitely
	public void confirmMessage(Vector<String> seqs,int timeout,HashMap<String,String> props) throws RpcException{
		boolean r_1 = false;
		RpcMessage m_2 = new RpcMessage(RpcMessage.CALL);
		m_2.ifidx = 3;
		m_2.opidx = 1;
		m_2.paramsize = 1;
		m_2.extra.setProperties(props);
		try{
			ByteArrayOutputStream bos_3 = new ByteArrayOutputStream();
			DataOutputStream dos_4 = new DataOutputStream(bos_3);
			SIDS_thlp c_5 = new SIDS_thlp(seqs);
			c_5.marshall(dos_4);
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
	
	public void confirmMessage_oneway(Vector<String> seqs,HashMap<String,String> props) throws RpcException{
		boolean r_1 = false;
		RpcMessage m_2 = new RpcMessage(RpcMessage.CALL|RpcMessage.ONEWAY);
		m_2.ifidx = 3;
		m_2.opidx = 1;
		m_2.paramsize = 1;
		m_2.extra.setProperties(props);
		try{
			ByteArrayOutputStream bos_3 = new ByteArrayOutputStream();
			DataOutputStream dos_4 = new DataOutputStream(bos_3);
			SIDS_thlp c_5 = new SIDS_thlp(seqs);
			c_5.marshall(dos_4);
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
	
	public void confirmMessage_async(Vector<String> seqs,IMessageServer_AsyncCallBack async,HashMap<String,String> props) throws RpcException{
		confirmMessage_async(seqs,async,props,null);
	}	
	
	public void confirmMessage_async(Vector<String> seqs,IMessageServer_AsyncCallBack async) throws RpcException{
		confirmMessage_async(seqs,async,null,null);
	}	
	
	public void confirmMessage_async(Vector<String> seqs,IMessageServer_AsyncCallBack async,HashMap<String,String> props,Object cookie) throws RpcException{
		boolean r_6 = false;
		RpcMessage m_7 = new RpcMessage(RpcMessage.CALL|RpcMessage.ASYNC);
		m_7.ifidx = 3;
		m_7.opidx = 1;
		m_7.paramsize = 1;
		m_7.extra.setProperties(props);
		m_7.cookie = cookie;
		try{
			ByteArrayOutputStream bos_8 = new ByteArrayOutputStream();
			DataOutputStream dos_9 = new DataOutputStream(bos_8);
			SIDS_thlp c_10 = new SIDS_thlp(seqs);
			c_10.marshall(dos_9);
			m_7.paramstream = bos_8.toByteArray();
			m_7.prx = this;
			m_7.async = async;
		}catch(Exception e){
			throw new RpcException(RpcConsts.RPCERROR_DATADIRTY,e.toString());
		}		
		r_6 = this.conn.sendMessage(m_7);
		if(!r_6){
			throw new RpcException(RpcConsts.RPCERROR_SENDFAILED);
		}		
	}	
	
	
}
