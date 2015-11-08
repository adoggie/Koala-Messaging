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

public class Notification_t{
// -- STRUCT -- 
	public  String type = "";
	public  String title = "";
	public  String content = "";
	public  String p1 = "";
	public  String p2 = "";
	
	//构造函数
	public Notification_t(){
		
	}	
	
	// return xml string
	public boolean marshall(DataOutputStream d){
		try{
			byte[] sb_1 = type.getBytes();
			d.writeInt(sb_1.length);
			d.write(sb_1,0,sb_1.length);
			byte[] sb_2 = title.getBytes();
			d.writeInt(sb_2.length);
			d.write(sb_2,0,sb_2.length);
			byte[] sb_3 = content.getBytes();
			d.writeInt(sb_3.length);
			d.write(sb_3,0,sb_3.length);
			byte[] sb_4 = p1.getBytes();
			d.writeInt(sb_4.length);
			d.write(sb_4,0,sb_4.length);
			byte[] sb_5 = p2.getBytes();
			d.writeInt(sb_5.length);
			d.write(sb_5,0,sb_5.length);
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
			this.type = new String(_sb_2);
			int v_3 = d.getInt();
			byte[] _sb_4 = new byte[v_3];
			d.get(_sb_4);
			this.title = new String(_sb_4);
			int v_5 = d.getInt();
			byte[] _sb_6 = new byte[v_5];
			d.get(_sb_6);
			this.content = new String(_sb_6);
			int v_7 = d.getInt();
			byte[] _sb_8 = new byte[v_7];
			d.get(_sb_8);
			this.p1 = new String(_sb_8);
			int v_9 = d.getInt();
			byte[] _sb_10 = new byte[v_9];
			d.get(_sb_10);
			this.p2 = new String(_sb_10);
		}catch(Exception e){
			tce.RpcCommunicator.instance().getLogger().error(e.getMessage());
			r = false;
			return r;
		}		
		return true;
	}	
	 // --  end function -- 
	
}
