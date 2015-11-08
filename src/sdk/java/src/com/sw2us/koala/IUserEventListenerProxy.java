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


public class IUserEventListenerProxy extends RpcProxyBase{
	//# -- INTERFACE PROXY -- 
	
	public IUserEventListenerProxy(RpcConnection conn){
		this.conn = conn;
	}	
	
	public static IUserEventListenerProxy create(String host,int port,Boolean ssl_enable){
		int type = RpcConsts.CONNECTION_SOCK;
		if (ssl_enable) type |= RpcConsts.CONNECTION_SSL;
		RpcConnection conn = RpcCommunicator.instance().createConnection(type,host,port);
		IUserEventListenerProxy prx = new IUserEventListenerProxy(conn);
		return prx;
	}	
	public static IUserEventListenerProxy createWithProxy(RpcProxyBase proxy){
		IUserEventListenerProxy prx = new IUserEventListenerProxy(proxy.conn);
		return prx;
	}	
	
	public void destroy(){
		try{
			conn.close();
		}catch(Exception e){
			RpcCommunicator.instance().getLogger().error(e.getMessage());
		}		
	}	
	
	public void onUserOnline(String userid,String gws_id,Integer device) throws RpcException{
onUserOnline(userid,gws_id,device,tce.RpcCommunicator.instance().getProperty_DefaultCallWaitTime(),null);		
	}	
	// timeout - msec ,  0 means waiting infinitely
	public void onUserOnline(String userid,String gws_id,Integer device,int timeout,HashMap<String,String> props) throws RpcException{
		boolean r_1 = false;
		RpcMessage m_2 = new RpcMessage(RpcMessage.CALL);
		m_2.ifidx = 1;
		m_2.opidx = 0;
		m_2.paramsize = 3;
		m_2.extra.setProperties(props);
		try{
			ByteArrayOutputStream bos_3 = new ByteArrayOutputStream();
			DataOutputStream dos_4 = new DataOutputStream(bos_3);
			byte[] sb_5 = userid.getBytes();
			dos_4.writeInt(sb_5.length);
			dos_4.write(sb_5,0,sb_5.length);
			byte[] sb_6 = gws_id.getBytes();
			dos_4.writeInt(sb_6.length);
			dos_4.write(sb_6,0,sb_6.length);
			dos_4.writeInt(device);
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
	
	public void onUserOnline_oneway(String userid,String gws_id,Integer device,HashMap<String,String> props) throws RpcException{
		boolean r_1 = false;
		RpcMessage m_2 = new RpcMessage(RpcMessage.CALL|RpcMessage.ONEWAY);
		m_2.ifidx = 1;
		m_2.opidx = 0;
		m_2.paramsize = 3;
		m_2.extra.setProperties(props);
		try{
			ByteArrayOutputStream bos_3 = new ByteArrayOutputStream();
			DataOutputStream dos_4 = new DataOutputStream(bos_3);
			byte[] sb_5 = userid.getBytes();
			dos_4.writeInt(sb_5.length);
			dos_4.write(sb_5,0,sb_5.length);
			byte[] sb_6 = gws_id.getBytes();
			dos_4.writeInt(sb_6.length);
			dos_4.write(sb_6,0,sb_6.length);
			dos_4.writeInt(device);
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
	
	public void onUserOnline_async(String userid,String gws_id,Integer device,IUserEventListener_AsyncCallBack async,HashMap<String,String> props) throws RpcException{
		onUserOnline_async(userid,gws_id,device,async,props,null);
	}	
	
	public void onUserOnline_async(String userid,String gws_id,Integer device,IUserEventListener_AsyncCallBack async) throws RpcException{
		onUserOnline_async(userid,gws_id,device,async,null,null);
	}	
	
	public void onUserOnline_async(String userid,String gws_id,Integer device,IUserEventListener_AsyncCallBack async,HashMap<String,String> props,Object cookie) throws RpcException{
		boolean r_7 = false;
		RpcMessage m_8 = new RpcMessage(RpcMessage.CALL|RpcMessage.ASYNC);
		m_8.ifidx = 1;
		m_8.opidx = 0;
		m_8.paramsize = 3;
		m_8.extra.setProperties(props);
		m_8.cookie = cookie;
		try{
			ByteArrayOutputStream bos_9 = new ByteArrayOutputStream();
			DataOutputStream dos_10 = new DataOutputStream(bos_9);
			byte[] sb_11 = userid.getBytes();
			dos_10.writeInt(sb_11.length);
			dos_10.write(sb_11,0,sb_11.length);
			byte[] sb_12 = gws_id.getBytes();
			dos_10.writeInt(sb_12.length);
			dos_10.write(sb_12,0,sb_12.length);
			dos_10.writeInt(device);
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
	
	
	
	public void onUserOffline(String userid,String gws_id,Integer device) throws RpcException{
onUserOffline(userid,gws_id,device,tce.RpcCommunicator.instance().getProperty_DefaultCallWaitTime(),null);		
	}	
	// timeout - msec ,  0 means waiting infinitely
	public void onUserOffline(String userid,String gws_id,Integer device,int timeout,HashMap<String,String> props) throws RpcException{
		boolean r_1 = false;
		RpcMessage m_2 = new RpcMessage(RpcMessage.CALL);
		m_2.ifidx = 1;
		m_2.opidx = 1;
		m_2.paramsize = 3;
		m_2.extra.setProperties(props);
		try{
			ByteArrayOutputStream bos_3 = new ByteArrayOutputStream();
			DataOutputStream dos_4 = new DataOutputStream(bos_3);
			byte[] sb_5 = userid.getBytes();
			dos_4.writeInt(sb_5.length);
			dos_4.write(sb_5,0,sb_5.length);
			byte[] sb_6 = gws_id.getBytes();
			dos_4.writeInt(sb_6.length);
			dos_4.write(sb_6,0,sb_6.length);
			dos_4.writeInt(device);
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
	
	public void onUserOffline_oneway(String userid,String gws_id,Integer device,HashMap<String,String> props) throws RpcException{
		boolean r_1 = false;
		RpcMessage m_2 = new RpcMessage(RpcMessage.CALL|RpcMessage.ONEWAY);
		m_2.ifidx = 1;
		m_2.opidx = 1;
		m_2.paramsize = 3;
		m_2.extra.setProperties(props);
		try{
			ByteArrayOutputStream bos_3 = new ByteArrayOutputStream();
			DataOutputStream dos_4 = new DataOutputStream(bos_3);
			byte[] sb_5 = userid.getBytes();
			dos_4.writeInt(sb_5.length);
			dos_4.write(sb_5,0,sb_5.length);
			byte[] sb_6 = gws_id.getBytes();
			dos_4.writeInt(sb_6.length);
			dos_4.write(sb_6,0,sb_6.length);
			dos_4.writeInt(device);
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
	
	public void onUserOffline_async(String userid,String gws_id,Integer device,IUserEventListener_AsyncCallBack async,HashMap<String,String> props) throws RpcException{
		onUserOffline_async(userid,gws_id,device,async,props,null);
	}	
	
	public void onUserOffline_async(String userid,String gws_id,Integer device,IUserEventListener_AsyncCallBack async) throws RpcException{
		onUserOffline_async(userid,gws_id,device,async,null,null);
	}	
	
	public void onUserOffline_async(String userid,String gws_id,Integer device,IUserEventListener_AsyncCallBack async,HashMap<String,String> props,Object cookie) throws RpcException{
		boolean r_7 = false;
		RpcMessage m_8 = new RpcMessage(RpcMessage.CALL|RpcMessage.ASYNC);
		m_8.ifidx = 1;
		m_8.opidx = 1;
		m_8.paramsize = 3;
		m_8.extra.setProperties(props);
		m_8.cookie = cookie;
		try{
			ByteArrayOutputStream bos_9 = new ByteArrayOutputStream();
			DataOutputStream dos_10 = new DataOutputStream(bos_9);
			byte[] sb_11 = userid.getBytes();
			dos_10.writeInt(sb_11.length);
			dos_10.write(sb_11,0,sb_11.length);
			byte[] sb_12 = gws_id.getBytes();
			dos_10.writeInt(sb_12.length);
			dos_10.write(sb_12,0,sb_12.length);
			dos_10.writeInt(device);
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
	
	
}
