package com.sw2us.koala;

//import tce.*;
//import javax.xml.parsers.*;
//import org.w3c.dom.*;
//import java.io.*;
//import java.nio.*;
//import java.util.*;
	

import com.sw2us.koala.*;
import java.io.*;
import java.nio.*;
import java.util.*;

public class MessageStyle_t{
// -- STRUCT -- 
	public  Integer builder_id = Integer.valueOf(0);
	public  Integer ring = Integer.valueOf(0);
	
	//构造函数
	public MessageStyle_t(){
		
	}	
	
	// return xml string
	public boolean marshall(DataOutputStream d){
		try{
			d.writeInt(builder_id);
			d.writeInt(ring);
		}catch(Exception e){
			return false;
		}		
		return true;
	}	
	
	public boolean unmarshall(ByteBuffer d){
		boolean r = false;
		try{
			this.builder_id = d.getInt();
			this.ring = d.getInt();
		}catch(Exception e){
			tce.RpcCommunicator.instance().getLogger().error(e.getMessage());
			r = false;
			return r;
		}		
		return true;
	}	
	 // --  end function -- 
	
}
