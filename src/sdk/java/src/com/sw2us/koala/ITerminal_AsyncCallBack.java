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

public class ITerminal_AsyncCallBack extends RpcAsyncCallBackBase{
	// following functions should be ovrrided in user code.
	public void onSimpleText(RpcProxyBase proxy,Object cookie){
	}	
	
	public void onMessage(RpcProxyBase proxy,Object cookie){
	}	
	
	public void onError(RpcProxyBase proxy,Object cookie){
	}	
	
	public void onSystemNotification(RpcProxyBase proxy,Object cookie){
	}	
	
	@Override
	public void callReturn(RpcMessage m1,RpcMessage m2){
		boolean r = false;
		ByteBuffer d = ByteBuffer.wrap(m2.paramstream);
		if(m1.opidx == 0){
			onSimpleText(m1.prx,m1.cookie);
		}		
		if(m1.opidx == 1){
			onMessage(m1.prx,m1.cookie);
		}		
		if(m1.opidx == 2){
			onError(m1.prx,m1.cookie);
		}		
		if(m1.opidx == 3){
			onSystemNotification(m1.prx,m1.cookie);
		}		
	}	
}
