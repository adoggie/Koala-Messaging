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

public class CallReturn_t{
// -- STRUCT -- 
	public  Error_t error = new Error_t();
	public  String value = "";
	public  String delta = "";
	
	//构造函数
	public CallReturn_t(){
		
	}	
	
	// return xml string
	public boolean marshall(DataOutputStream d){
		try{
			error.marshall(d);
			byte[] sb_1 = value.getBytes();
			d.writeInt(sb_1.length);
			d.write(sb_1,0,sb_1.length);
			byte[] sb_2 = delta.getBytes();
			d.writeInt(sb_2.length);
			d.write(sb_2,0,sb_2.length);
		}catch(Exception e){
			return false;
		}		
		return true;
	}	
	
	public boolean unmarshall(ByteBuffer d){
		boolean r = false;
		try{
			r = this.error.unmarshall(d);
			if(!r){return false;}
			int v_1 = d.getInt();
			byte[] _sb_2 = new byte[v_1];
			d.get(_sb_2);
			this.value = new String(_sb_2);
			int v_3 = d.getInt();
			byte[] _sb_4 = new byte[v_3];
			d.get(_sb_4);
			this.delta = new String(_sb_4);
		}catch(Exception e){
			tce.RpcCommunicator.instance().getLogger().error(e.getMessage());
			r = false;
			return r;
		}		
		return true;
	}	
	 // --  end function -- 
	
}
