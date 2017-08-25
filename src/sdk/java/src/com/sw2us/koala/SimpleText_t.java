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

public class SimpleText_t{
// -- STRUCT -- 
	public  String seq = "";
	public  String sender_id = "";
	public  String send_time = "";
	public  String title = "";
	public  String content = "";
	
	//构造函数
	public SimpleText_t(){
		
	}	
	
	// return xml string
	public boolean marshall(DataOutputStream d){
		try{
			byte[] sb_1 = seq.getBytes();
			d.writeInt(sb_1.length);
			d.write(sb_1,0,sb_1.length);
			byte[] sb_2 = sender_id.getBytes();
			d.writeInt(sb_2.length);
			d.write(sb_2,0,sb_2.length);
			byte[] sb_3 = send_time.getBytes();
			d.writeInt(sb_3.length);
			d.write(sb_3,0,sb_3.length);
			byte[] sb_4 = title.getBytes();
			d.writeInt(sb_4.length);
			d.write(sb_4,0,sb_4.length);
			byte[] sb_5 = content.getBytes();
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
			this.seq = new String(_sb_2);
			int v_3 = d.getInt();
			byte[] _sb_4 = new byte[v_3];
			d.get(_sb_4);
			this.sender_id = new String(_sb_4);
			int v_5 = d.getInt();
			byte[] _sb_6 = new byte[v_5];
			d.get(_sb_6);
			this.send_time = new String(_sb_6);
			int v_7 = d.getInt();
			byte[] _sb_8 = new byte[v_7];
			d.get(_sb_8);
			this.title = new String(_sb_8);
			int v_9 = d.getInt();
			byte[] _sb_10 = new byte[v_9];
			d.get(_sb_10);
			this.content = new String(_sb_10);
		}catch(Exception e){
			tce.RpcCommunicator.instance().getLogger().error(e.getMessage());
			r = false;
			return r;
		}		
		return true;
	}	
	 // --  end function -- 
	
}
