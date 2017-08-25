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

public class AuthToken_t{
// -- STRUCT -- 
	public  String user_id = "";
	public  String user_name = "";
	public  Long login_time = Long.valueOf(0);
	public  Long expire_time = Long.valueOf(0);
	public  Integer platform_type = Integer.valueOf(0);
	public  String device_id = "";
	
	//构造函数
	public AuthToken_t(){
		
	}	
	
	// return xml string
	public boolean marshall(DataOutputStream d){
		try{
			byte[] sb_1 = user_id.getBytes();
			d.writeInt(sb_1.length);
			d.write(sb_1,0,sb_1.length);
			byte[] sb_2 = user_name.getBytes();
			d.writeInt(sb_2.length);
			d.write(sb_2,0,sb_2.length);
			d.writeLong(login_time);
			d.writeLong(expire_time);
			d.writeInt(platform_type);
			byte[] sb_3 = device_id.getBytes();
			d.writeInt(sb_3.length);
			d.write(sb_3,0,sb_3.length);
		}catch(Exception e){
			return false;
		}		
		return true;
	}	
	
	public boolean unmarshall(ByteBuffer d){
		boolean r = false;
		try{
			int v_1 = d.getInt();
			byte[] _sb_2 = new byte[v_1];
			d.get(_sb_2);
			this.user_id = new String(_sb_2);
			int v_3 = d.getInt();
			byte[] _sb_4 = new byte[v_3];
			d.get(_sb_4);
			this.user_name = new String(_sb_4);
			this.login_time = d.getLong();
			this.expire_time = d.getLong();
			this.platform_type = d.getInt();
			int v_5 = d.getInt();
			byte[] _sb_6 = new byte[v_5];
			d.get(_sb_6);
			this.device_id = new String(_sb_6);
		}catch(Exception e){
			tce.RpcCommunicator.instance().getLogger().error(e.getMessage());
			r = false;
			return r;
		}		
		return true;
	}	
	 // --  end function -- 
	
}
