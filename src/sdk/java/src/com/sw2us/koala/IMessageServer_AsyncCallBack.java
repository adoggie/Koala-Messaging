package com.sw2us.koala;

//import tce.*;
//import javax.xml.parsers.*;
//import org.w3c.dom.*;
//import java.io.*;
//import java.nio.*;
//import java.util.*;
	

import com.sw2us.koala.*;
import tce.*;
import java.nio.*;
import java.util.*;

public class IMessageServer_AsyncCallBack extends RpcAsyncCallBackBase{
	// following functions should be ovrrided in user code.
	public void sendMessage(RpcProxyBase proxy,Object cookie){
	}	
	
	public void confirmMessage(RpcProxyBase proxy,Object cookie){
	}	
	
	@Override
	public void callReturn(RpcMessage m1,RpcMessage m2){
		boolean r = false;
		ByteBuffer d = ByteBuffer.wrap(m2.paramstream);
		if(m1.opidx == 0){
			sendMessage(m1.prx,m1.cookie);
		}		
		if(m1.opidx == 1){
			confirmMessage(m1.prx,m1.cookie);
		}		
	}	
}
