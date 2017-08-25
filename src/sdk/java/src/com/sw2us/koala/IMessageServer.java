package com.sw2us.koala;

//import tce.*;
//import javax.xml.parsers.*;
//import org.w3c.dom.*;
//import java.io.*;
//import java.nio.*;
//import java.util.*;
	
import tce.*;
import com.sw2us.koala.IMessageServer_delegate;
import com.sw2us.koala.*;
import java.util.*;

public class IMessageServer extends RpcServant{
	//# -- INTERFACE -- 
	public IMessageServer(){
		super();
		this.delegate = new IMessageServer_delegate(this);
	}	
	
	
	public void sendMessage(Vector<String> token_list,Message_t message,RpcContext ctx){
	}	
	
	public void confirmMessage(Vector<String> seqs,RpcContext ctx){
	}	
}
