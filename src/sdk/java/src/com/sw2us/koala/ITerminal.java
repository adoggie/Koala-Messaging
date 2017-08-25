package com.sw2us.koala;

//import tce.*;
//import javax.xml.parsers.*;
//import org.w3c.dom.*;
//import java.io.*;
//import java.nio.*;
//import java.util.*;
	
import tce.*;
import com.sw2us.koala.ITerminal_delegate;
import com.sw2us.koala.*;
import java.util.*;

public class ITerminal extends RpcServant{
	//# -- INTERFACE -- 
	public ITerminal(){
		super();
		this.delegate = new ITerminal_delegate(this);
	}	
	
	
	public void onSimpleText(SimpleText_t text,RpcContext ctx){
	}	
	
	public void onMessage(Message_t message,RpcContext ctx){
	}	
	
	public void onError(String errcode,String errmsg,RpcContext ctx){
	}	
	
	public void onSystemNotification(Notification_t notification,RpcContext ctx){
	}	
}
