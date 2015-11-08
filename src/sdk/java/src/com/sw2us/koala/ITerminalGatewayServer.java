package com.sw2us.koala;

//import tce.*;
//import javax.xml.parsers.*;
//import org.w3c.dom.*;
//import java.io.*;
//import java.nio.*;
//import java.util.*;
	
import tce.*;
import com.sw2us.koala.ITerminalGatewayServer_delegate;
import com.sw2us.koala.*;
import java.util.*;

public class ITerminalGatewayServer extends RpcServant{
	//# -- INTERFACE -- 
	public ITerminalGatewayServer(){
		super();
		this.delegate = new ITerminalGatewayServer_delegate(this);
	}	
	
	
	public void ping(RpcContext ctx){
	}	
}
