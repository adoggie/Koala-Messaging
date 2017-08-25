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

public class SIDS_thlp{
	//# -- SEQUENCE --
	
	public Vector<String> ds = null;
	public SIDS_thlp(Vector<String> ds){
		this.ds = ds;
	}	
	
	public boolean marshall(DataOutputStream d){
		try{
			d.writeInt(this.ds.size());
			for(String item : this.ds){
				byte[] sb_1 = item.getBytes();
				d.writeInt(sb_1.length);
				d.write(sb_1,0,sb_1.length);
			}			
		}catch(Exception e){
			return false;
		}		
		return true;
	}	
	
	public boolean unmarshall(ByteBuffer d){
		int _size_2 = 0;
		try{
			_size_2 = d.getInt();
			for(int _p=0;_p < _size_2;_p++){
				String _o = "";
				int v_4 = d.getInt();
				byte[] _sb_5 = new byte[v_4];
				d.get(_sb_5);
				_o = new String(_sb_5);
				this.ds.add(_o);
			}			
		}catch(Exception e){
			return false;
		}		
		return true;
	}	
	
}

