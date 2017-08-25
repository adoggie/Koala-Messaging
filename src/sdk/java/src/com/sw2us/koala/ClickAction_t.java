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

public class ClickAction_t{
// -- STRUCT -- 
	public  Integer act_type = Integer.valueOf(0);
	public  String url = "";
	public  Integer conform_on_url = Integer.valueOf(0);
	public  String activity = "";
	public  String intent = "";
	public  Integer intent_flag = Integer.valueOf(0);
	public  Integer pending_flag = Integer.valueOf(0);
	public  String package_name = "";
	public  String package_download_url = "";
	public  Integer confirm_on_package = Integer.valueOf(0);
	
	//构造函数
	public ClickAction_t(){
		
	}	
	
	// return xml string
	public boolean marshall(DataOutputStream d){
		try{
			d.writeInt(act_type);
			byte[] sb_1 = url.getBytes();
			d.writeInt(sb_1.length);
			d.write(sb_1,0,sb_1.length);
			d.writeInt(conform_on_url);
			byte[] sb_2 = activity.getBytes();
			d.writeInt(sb_2.length);
			d.write(sb_2,0,sb_2.length);
			byte[] sb_3 = intent.getBytes();
			d.writeInt(sb_3.length);
			d.write(sb_3,0,sb_3.length);
			d.writeInt(intent_flag);
			d.writeInt(pending_flag);
			byte[] sb_4 = package_name.getBytes();
			d.writeInt(sb_4.length);
			d.write(sb_4,0,sb_4.length);
			byte[] sb_5 = package_download_url.getBytes();
			d.writeInt(sb_5.length);
			d.write(sb_5,0,sb_5.length);
			d.writeInt(confirm_on_package);
		}catch(Exception e){
			return false;
		}		
		return true;
	}	
	
	public boolean unmarshall(ByteBuffer d){
		boolean r = false;
		try{
			this.act_type = d.getInt();
			int v_1 = d.getInt();
			byte[] _sb_2 = new byte[v_1];
			d.get(_sb_2);
			this.url = new String(_sb_2);
			this.conform_on_url = d.getInt();
			int v_3 = d.getInt();
			byte[] _sb_4 = new byte[v_3];
			d.get(_sb_4);
			this.activity = new String(_sb_4);
			int v_5 = d.getInt();
			byte[] _sb_6 = new byte[v_5];
			d.get(_sb_6);
			this.intent = new String(_sb_6);
			this.intent_flag = d.getInt();
			this.pending_flag = d.getInt();
			int v_7 = d.getInt();
			byte[] _sb_8 = new byte[v_7];
			d.get(_sb_8);
			this.package_name = new String(_sb_8);
			int v_9 = d.getInt();
			byte[] _sb_10 = new byte[v_9];
			d.get(_sb_10);
			this.package_download_url = new String(_sb_10);
			this.confirm_on_package = d.getInt();
		}catch(Exception e){
			tce.RpcCommunicator.instance().getLogger().error(e.getMessage());
			r = false;
			return r;
		}		
		return true;
	}	
	 // --  end function -- 
	
}
