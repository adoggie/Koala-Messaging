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

public class Error_t{
// -- STRUCT -- 
	public  Boolean succ = Boolean.valueOf(false);
	public  Integer code = Integer.valueOf(0);
	public  String msg = "";
	
	//构造函数
	public Error_t(){
		
	}	
	
	// return xml string
	public boolean marshall(DataOutputStream d){
		try{
			d.writeByte( succ.booleanValue()?1:0);
			d.writeInt(code);
			byte[] sb_1 = msg.getBytes();
			d.writeInt(sb_1.length);
			d.write(sb_1,0,sb_1.length);
		}catch(Exception e){
			return false;
		}		
		return true;
	}	
	
	public boolean unmarshall(ByteBuffer d){
		boolean r = false;
		try{
			byte v_1 = d.get();
			this.succ = v_1==0?false:true;
			this.code = d.getInt();
			int v_2 = d.getInt();
			byte[] _sb_3 = new byte[v_2];
			d.get(_sb_3);
			this.msg = new String(_sb_3);
		}catch(Exception e){
			tce.RpcCommunicator.instance().getLogger().error(e.getMessage());
			r = false;
			return r;
		}		
		return true;
	}	
	 // --  end function -- 
	
}
