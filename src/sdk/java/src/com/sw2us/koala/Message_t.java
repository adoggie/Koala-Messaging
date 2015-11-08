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

public class Message_t{
// -- STRUCT -- 
	public  String seq = "";
	public  String sender_id = "";
	public  String sent_time = "";
	public  String title = "";
	public  String content = "";
	public  String expire_time = "";
	public  String send_time = "";
	public  String accept_time = "";
	public  Integer type = Integer.valueOf(0);
	public  MessageStyle_t style = new MessageStyle_t();
	public  ClickAction_t action = new ClickAction_t();
	public  String custom = "";
	public  Integer loop_times = Integer.valueOf(0);
	public  Integer loop_inerval = Integer.valueOf(0);
	public  String alert = "";
	public  Integer badge = Integer.valueOf(0);
	public  String sound = "";
	public  String category = "";
	public  String raw = "";
	
	//构造函数
	public Message_t(){
		
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
			byte[] sb_3 = sent_time.getBytes();
			d.writeInt(sb_3.length);
			d.write(sb_3,0,sb_3.length);
			byte[] sb_4 = title.getBytes();
			d.writeInt(sb_4.length);
			d.write(sb_4,0,sb_4.length);
			byte[] sb_5 = content.getBytes();
			d.writeInt(sb_5.length);
			d.write(sb_5,0,sb_5.length);
			byte[] sb_6 = expire_time.getBytes();
			d.writeInt(sb_6.length);
			d.write(sb_6,0,sb_6.length);
			byte[] sb_7 = send_time.getBytes();
			d.writeInt(sb_7.length);
			d.write(sb_7,0,sb_7.length);
			byte[] sb_8 = accept_time.getBytes();
			d.writeInt(sb_8.length);
			d.write(sb_8,0,sb_8.length);
			d.writeInt(type);
			style.marshall(d);
			action.marshall(d);
			byte[] sb_9 = custom.getBytes();
			d.writeInt(sb_9.length);
			d.write(sb_9,0,sb_9.length);
			d.writeInt(loop_times);
			d.writeInt(loop_inerval);
			byte[] sb_10 = alert.getBytes();
			d.writeInt(sb_10.length);
			d.write(sb_10,0,sb_10.length);
			d.writeInt(badge);
			byte[] sb_11 = sound.getBytes();
			d.writeInt(sb_11.length);
			d.write(sb_11,0,sb_11.length);
			byte[] sb_12 = category.getBytes();
			d.writeInt(sb_12.length);
			d.write(sb_12,0,sb_12.length);
			byte[] sb_13 = raw.getBytes();
			d.writeInt(sb_13.length);
			d.write(sb_13,0,sb_13.length);
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
			this.sent_time = new String(_sb_6);
			int v_7 = d.getInt();
			byte[] _sb_8 = new byte[v_7];
			d.get(_sb_8);
			this.title = new String(_sb_8);
			int v_9 = d.getInt();
			byte[] _sb_10 = new byte[v_9];
			d.get(_sb_10);
			this.content = new String(_sb_10);
			int v_11 = d.getInt();
			byte[] _sb_12 = new byte[v_11];
			d.get(_sb_12);
			this.expire_time = new String(_sb_12);
			int v_13 = d.getInt();
			byte[] _sb_14 = new byte[v_13];
			d.get(_sb_14);
			this.send_time = new String(_sb_14);
			int v_15 = d.getInt();
			byte[] _sb_16 = new byte[v_15];
			d.get(_sb_16);
			this.accept_time = new String(_sb_16);
			this.type = d.getInt();
			r = this.style.unmarshall(d);
			if(!r){return false;}
			r = this.action.unmarshall(d);
			if(!r){return false;}
			int v_17 = d.getInt();
			byte[] _sb_18 = new byte[v_17];
			d.get(_sb_18);
			this.custom = new String(_sb_18);
			this.loop_times = d.getInt();
			this.loop_inerval = d.getInt();
			int v_19 = d.getInt();
			byte[] _sb_20 = new byte[v_19];
			d.get(_sb_20);
			this.alert = new String(_sb_20);
			this.badge = d.getInt();
			int v_21 = d.getInt();
			byte[] _sb_22 = new byte[v_21];
			d.get(_sb_22);
			this.sound = new String(_sb_22);
			int v_23 = d.getInt();
			byte[] _sb_24 = new byte[v_23];
			d.get(_sb_24);
			this.category = new String(_sb_24);
			int v_25 = d.getInt();
			byte[] _sb_26 = new byte[v_25];
			d.get(_sb_26);
			this.raw = new String(_sb_26);
		}catch(Exception e){
			tce.RpcCommunicator.instance().getLogger().error(e.getMessage());
			r = false;
			return r;
		}		
		return true;
	}	
	 // --  end function -- 
	
}
