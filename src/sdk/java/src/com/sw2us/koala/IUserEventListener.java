package com.sw2us.koala;

//import tce.*;
//import javax.xml.parsers.*;
//import org.w3c.dom.*;
//import java.io.*;
//import java.nio.*;
//import java.util.*;
	
import tce.*;
import com.sw2us.koala.IUserEventListener_delegate;
import com.sw2us.koala.*;
import java.util.*;

public class IUserEventListener extends RpcServant{
	//# -- INTERFACE -- 
	public IUserEventListener(){
		super();
		this.delegate = new IUserEventListener_delegate(this);
	}	
	
	
	public void onUserOnline(String userid,String gws_id,Integer device,RpcContext ctx){
	}	
	
	public void onUserOffline(String userid,String gws_id,Integer device,RpcContext ctx){
	}	
}
