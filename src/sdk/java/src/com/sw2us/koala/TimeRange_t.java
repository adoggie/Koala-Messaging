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

public class TimeRange_t{
// -- STRUCT -- 
	public  Long start = Long.valueOf(0);
	public  Long end = Long.valueOf(0);
	
	//构造函数
	public TimeRange_t(){
		
	}	
	
	// return xml string
	public boolean marshall(DataOutputStream d){
		try{
			d.writeLong(start);
			d.writeLong(end);
		}catch(Exception e){
			return false;
		}		
		return true;
	}	
	
	public boolean unmarshall(ByteBuffer d){
		boolean r = false;
		try{
			this.start = d.getLong();
			this.end = d.getLong();
		}catch(Exception e){
			tce.RpcCommunicator.instance().getLogger().error(e.getMessage());
			r = false;
			return r;
		}		
		return true;
	}	
	 // --  end function -- 
	
}
