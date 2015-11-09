
// -- coding:utf-8 --
//---------------------------------
//  TCE
//  Tiny Communication Engine
//
//  sw2us.com copyright @2012
//  bin.zhang@sw2us.com / qq:24509826
//---------------------------------

	
define("koala",["tce"],function(tce){


function SIDS_thlp(ds){
	//# -- SEQUENCE --
	
	this.ds = ds; // Array()
	
	this.getsize = function(){
		var size =4;
		for(var p=0;p<this.ds.length;p++){
			var _bx_1 =this.ds[p];
			var _sb_2 = tce.utf16to8(_bx_1);
			size+= 4 + _sb_2.getBytes().length;
		}		
		return size;
	}	;	
	
	this.marshall = function(view,pos){
		view.setUint32(pos,this.ds.length);
		pos+=4;
		for(var n=0;n<this.ds.length;n++){
			var _sb_1 = tce.utf16to8(this.ds[n]).getBytes();
			view.setInt32(pos,_sb_1.length);
			pos+=4;
			var _sb_2 = new Uint8Array(view.buffer);
			_sb_2.set(_sb_1,pos);
			pos += _sb_1.length;
		}		
		return pos;
	}	;	
	
	this.unmarshall = function(view,pos){
		var _size_1 = view.getUint32(pos);
		pos+=4;
		for(var _p=0;_p < _size_1;_p++){
			var _o = '';
			var _sb_3 = view.getUint32(pos);
			pos+=4;
			_o = view.buffer.slice(pos,pos+_sb_3);
			// this var is Uint8Array,should convert to String!!
			pos+= _sb_3;
			_o = String.fromCharCode.apply(null, _o.getBytes());
			_o = tce.utf8to16(_o);
			this.ds.push(_o);
		}		
		return pos;
	}	;	
	
}




function Error_t(){
// -- STRUCT -- 
	this.succ = false; 
	this.code = 0; 
	this.msg = ''; 
	
	this.getsize = function(){
		var size =0;
		size+= 1;
		size+= 4;
		var _sb_1 = tce.utf16to8(this.msg);
		size+= 4 + _sb_1.getBytes().length;
		return size;
	}	;	
	
	// 
	this.marshall = function(view,pos){
		view.setUint8(pos,this.succ==true?1:0);
		pos+=1;
		view.setInt32(pos,this.code);
		pos+=4;
		var _sb_1 = tce.utf16to8(this.msg).getBytes();
		view.setInt32(pos,_sb_1.length);
		pos+=4;
		var _sb_2 = new Uint8Array(view.buffer);
		_sb_2.set(_sb_1,pos);
		pos += _sb_1.length;
		return pos;
	}	;	
	
	this.unmarshall = function(view,pos){
		var _b_1 = view.getInt8(pos);
		this.succ = _b_1==0?false:true;
		pos+=1;
		this.code = view.getInt32(pos);
		pos+=4;
		var _sb_2 = view.getUint32(pos);
		pos+=4;
		this.msg = view.buffer.slice(pos,pos+_sb_2);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_2;
		this.msg = String.fromCharCode.apply(null, this.msg.getBytes());
		this.msg = tce.utf8to16(this.msg);
		return pos;
	}	;	
	 // --  end function -- 
	
}




function CallReturn_t(){
// -- STRUCT -- 
	this.error = new Error_t(); 
	this.value = ''; 
	this.delta = ''; 
	
	this.getsize = function(){
		var size =0;
		size+=this.error.getsize();
		var _sb_1 = tce.utf16to8(this.value);
		size+= 4 + _sb_1.getBytes().length;
		var _sb_2 = tce.utf16to8(this.delta);
		size+= 4 + _sb_2.getBytes().length;
		return size;
	}	;	
	
	// 
	this.marshall = function(view,pos){
		pos= this.error.marshall(view,pos);
		var _sb_1 = tce.utf16to8(this.value).getBytes();
		view.setInt32(pos,_sb_1.length);
		pos+=4;
		var _sb_2 = new Uint8Array(view.buffer);
		_sb_2.set(_sb_1,pos);
		pos += _sb_1.length;
		var _sb_3 = tce.utf16to8(this.delta).getBytes();
		view.setInt32(pos,_sb_3.length);
		pos+=4;
		var _sb_4 = new Uint8Array(view.buffer);
		_sb_4.set(_sb_3,pos);
		pos += _sb_3.length;
		return pos;
	}	;	
	
	this.unmarshall = function(view,pos){
		pos = this.error.unmarshall(view,pos);
		var _sb_1 = view.getUint32(pos);
		pos+=4;
		this.value = view.buffer.slice(pos,pos+_sb_1);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_1;
		this.value = String.fromCharCode.apply(null, this.value.getBytes());
		this.value = tce.utf8to16(this.value);
		var _sb_3 = view.getUint32(pos);
		pos+=4;
		this.delta = view.buffer.slice(pos,pos+_sb_3);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_3;
		this.delta = String.fromCharCode.apply(null, this.delta.getBytes());
		this.delta = tce.utf8to16(this.delta);
		return pos;
	}	;	
	 // --  end function -- 
	
}




function TimeRange_t(){
// -- STRUCT -- 
	this.start = 0; 
	this.end = 0; 
	
	this.getsize = function(){
		var size =0;
		size+= 8;
		size+= 8;
		return size;
	}	;	
	
	// 
	this.marshall = function(view,pos){
		view.setFloat64(pos,this.start);
		pos+=8;
		view.setFloat64(pos,this.end);
		pos+=8;
		return pos;
	}	;	
	
	this.unmarshall = function(view,pos){
		this.start = view.getFloat64(pos);
		pos+=8;
		this.end = view.getFloat64(pos);
		pos+=8;
		return pos;
	}	;	
	 // --  end function -- 
	
}




function AuthToken_t(){
// -- STRUCT -- 
	this.user_id = ''; 
	this.user_name = ''; 
	this.login_time = 0; 
	this.expire_time = 0; 
	this.platform_type = 0; 
	this.device_id = ''; 
	
	this.getsize = function(){
		var size =0;
		var _sb_1 = tce.utf16to8(this.user_id);
		size+= 4 + _sb_1.getBytes().length;
		var _sb_2 = tce.utf16to8(this.user_name);
		size+= 4 + _sb_2.getBytes().length;
		size+= 8;
		size+= 8;
		size+= 4;
		var _sb_3 = tce.utf16to8(this.device_id);
		size+= 4 + _sb_3.getBytes().length;
		return size;
	}	;	
	
	// 
	this.marshall = function(view,pos){
		var _sb_1 = tce.utf16to8(this.user_id).getBytes();
		view.setInt32(pos,_sb_1.length);
		pos+=4;
		var _sb_2 = new Uint8Array(view.buffer);
		_sb_2.set(_sb_1,pos);
		pos += _sb_1.length;
		var _sb_3 = tce.utf16to8(this.user_name).getBytes();
		view.setInt32(pos,_sb_3.length);
		pos+=4;
		var _sb_4 = new Uint8Array(view.buffer);
		_sb_4.set(_sb_3,pos);
		pos += _sb_3.length;
		view.setFloat64(pos,this.login_time);
		pos+=8;
		view.setFloat64(pos,this.expire_time);
		pos+=8;
		view.setInt32(pos,this.platform_type);
		pos+=4;
		var _sb_5 = tce.utf16to8(this.device_id).getBytes();
		view.setInt32(pos,_sb_5.length);
		pos+=4;
		var _sb_6 = new Uint8Array(view.buffer);
		_sb_6.set(_sb_5,pos);
		pos += _sb_5.length;
		return pos;
	}	;	
	
	this.unmarshall = function(view,pos){
		var _sb_1 = view.getUint32(pos);
		pos+=4;
		this.user_id = view.buffer.slice(pos,pos+_sb_1);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_1;
		this.user_id = String.fromCharCode.apply(null, this.user_id.getBytes());
		this.user_id = tce.utf8to16(this.user_id);
		var _sb_3 = view.getUint32(pos);
		pos+=4;
		this.user_name = view.buffer.slice(pos,pos+_sb_3);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_3;
		this.user_name = String.fromCharCode.apply(null, this.user_name.getBytes());
		this.user_name = tce.utf8to16(this.user_name);
		this.login_time = view.getFloat64(pos);
		pos+=8;
		this.expire_time = view.getFloat64(pos);
		pos+=8;
		this.platform_type = view.getInt32(pos);
		pos+=4;
		var _sb_5 = view.getUint32(pos);
		pos+=4;
		this.device_id = view.buffer.slice(pos,pos+_sb_5);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_5;
		this.device_id = String.fromCharCode.apply(null, this.device_id.getBytes());
		this.device_id = tce.utf8to16(this.device_id);
		return pos;
	}	;	
	 // --  end function -- 
	
}




function MessageStyle_t(){
// -- STRUCT -- 
	this.builder_id = 0; 
	this.ring = 0; 
	
	this.getsize = function(){
		var size =0;
		size+= 4;
		size+= 4;
		return size;
	}	;	
	
	// 
	this.marshall = function(view,pos){
		view.setInt32(pos,this.builder_id);
		pos+=4;
		view.setInt32(pos,this.ring);
		pos+=4;
		return pos;
	}	;	
	
	this.unmarshall = function(view,pos){
		this.builder_id = view.getInt32(pos);
		pos+=4;
		this.ring = view.getInt32(pos);
		pos+=4;
		return pos;
	}	;	
	 // --  end function -- 
	
}




function ClickAction_t(){
// -- STRUCT -- 
	this.act_type = 0; 
	this.url = ''; 
	this.conform_on_url = 0; 
	this.activity = ''; 
	this.intent = ''; 
	this.intent_flag = 0; 
	this.pending_flag = 0; 
	this.package_name = ''; 
	this.package_download_url = ''; 
	this.confirm_on_package = 0; 
	
	this.getsize = function(){
		var size =0;
		size+= 4;
		var _sb_1 = tce.utf16to8(this.url);
		size+= 4 + _sb_1.getBytes().length;
		size+= 4;
		var _sb_2 = tce.utf16to8(this.activity);
		size+= 4 + _sb_2.getBytes().length;
		var _sb_3 = tce.utf16to8(this.intent);
		size+= 4 + _sb_3.getBytes().length;
		size+= 4;
		size+= 4;
		var _sb_4 = tce.utf16to8(this.package_name);
		size+= 4 + _sb_4.getBytes().length;
		var _sb_5 = tce.utf16to8(this.package_download_url);
		size+= 4 + _sb_5.getBytes().length;
		size+= 4;
		return size;
	}	;	
	
	// 
	this.marshall = function(view,pos){
		view.setInt32(pos,this.act_type);
		pos+=4;
		var _sb_1 = tce.utf16to8(this.url).getBytes();
		view.setInt32(pos,_sb_1.length);
		pos+=4;
		var _sb_2 = new Uint8Array(view.buffer);
		_sb_2.set(_sb_1,pos);
		pos += _sb_1.length;
		view.setInt32(pos,this.conform_on_url);
		pos+=4;
		var _sb_3 = tce.utf16to8(this.activity).getBytes();
		view.setInt32(pos,_sb_3.length);
		pos+=4;
		var _sb_4 = new Uint8Array(view.buffer);
		_sb_4.set(_sb_3,pos);
		pos += _sb_3.length;
		var _sb_5 = tce.utf16to8(this.intent).getBytes();
		view.setInt32(pos,_sb_5.length);
		pos+=4;
		var _sb_6 = new Uint8Array(view.buffer);
		_sb_6.set(_sb_5,pos);
		pos += _sb_5.length;
		view.setInt32(pos,this.intent_flag);
		pos+=4;
		view.setInt32(pos,this.pending_flag);
		pos+=4;
		var _sb_7 = tce.utf16to8(this.package_name).getBytes();
		view.setInt32(pos,_sb_7.length);
		pos+=4;
		var _sb_8 = new Uint8Array(view.buffer);
		_sb_8.set(_sb_7,pos);
		pos += _sb_7.length;
		var _sb_9 = tce.utf16to8(this.package_download_url).getBytes();
		view.setInt32(pos,_sb_9.length);
		pos+=4;
		var _sb_10 = new Uint8Array(view.buffer);
		_sb_10.set(_sb_9,pos);
		pos += _sb_9.length;
		view.setInt32(pos,this.confirm_on_package);
		pos+=4;
		return pos;
	}	;	
	
	this.unmarshall = function(view,pos){
		this.act_type = view.getInt32(pos);
		pos+=4;
		var _sb_1 = view.getUint32(pos);
		pos+=4;
		this.url = view.buffer.slice(pos,pos+_sb_1);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_1;
		this.url = String.fromCharCode.apply(null, this.url.getBytes());
		this.url = tce.utf8to16(this.url);
		this.conform_on_url = view.getInt32(pos);
		pos+=4;
		var _sb_3 = view.getUint32(pos);
		pos+=4;
		this.activity = view.buffer.slice(pos,pos+_sb_3);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_3;
		this.activity = String.fromCharCode.apply(null, this.activity.getBytes());
		this.activity = tce.utf8to16(this.activity);
		var _sb_5 = view.getUint32(pos);
		pos+=4;
		this.intent = view.buffer.slice(pos,pos+_sb_5);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_5;
		this.intent = String.fromCharCode.apply(null, this.intent.getBytes());
		this.intent = tce.utf8to16(this.intent);
		this.intent_flag = view.getInt32(pos);
		pos+=4;
		this.pending_flag = view.getInt32(pos);
		pos+=4;
		var _sb_7 = view.getUint32(pos);
		pos+=4;
		this.package_name = view.buffer.slice(pos,pos+_sb_7);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_7;
		this.package_name = String.fromCharCode.apply(null, this.package_name.getBytes());
		this.package_name = tce.utf8to16(this.package_name);
		var _sb_9 = view.getUint32(pos);
		pos+=4;
		this.package_download_url = view.buffer.slice(pos,pos+_sb_9);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_9;
		this.package_download_url = String.fromCharCode.apply(null, this.package_download_url.getBytes());
		this.package_download_url = tce.utf8to16(this.package_download_url);
		this.confirm_on_package = view.getInt32(pos);
		pos+=4;
		return pos;
	}	;	
	 // --  end function -- 
	
}




function SimpleText_t(){
// -- STRUCT -- 
	this.seq = ''; 
	this.sender_id = ''; 
	this.send_time = ''; 
	this.title = ''; 
	this.content = ''; 
	
	this.getsize = function(){
		var size =0;
		var _sb_1 = tce.utf16to8(this.seq);
		size+= 4 + _sb_1.getBytes().length;
		var _sb_2 = tce.utf16to8(this.sender_id);
		size+= 4 + _sb_2.getBytes().length;
		var _sb_3 = tce.utf16to8(this.send_time);
		size+= 4 + _sb_3.getBytes().length;
		var _sb_4 = tce.utf16to8(this.title);
		size+= 4 + _sb_4.getBytes().length;
		var _sb_5 = tce.utf16to8(this.content);
		size+= 4 + _sb_5.getBytes().length;
		return size;
	}	;	
	
	// 
	this.marshall = function(view,pos){
		var _sb_1 = tce.utf16to8(this.seq).getBytes();
		view.setInt32(pos,_sb_1.length);
		pos+=4;
		var _sb_2 = new Uint8Array(view.buffer);
		_sb_2.set(_sb_1,pos);
		pos += _sb_1.length;
		var _sb_3 = tce.utf16to8(this.sender_id).getBytes();
		view.setInt32(pos,_sb_3.length);
		pos+=4;
		var _sb_4 = new Uint8Array(view.buffer);
		_sb_4.set(_sb_3,pos);
		pos += _sb_3.length;
		var _sb_5 = tce.utf16to8(this.send_time).getBytes();
		view.setInt32(pos,_sb_5.length);
		pos+=4;
		var _sb_6 = new Uint8Array(view.buffer);
		_sb_6.set(_sb_5,pos);
		pos += _sb_5.length;
		var _sb_7 = tce.utf16to8(this.title).getBytes();
		view.setInt32(pos,_sb_7.length);
		pos+=4;
		var _sb_8 = new Uint8Array(view.buffer);
		_sb_8.set(_sb_7,pos);
		pos += _sb_7.length;
		var _sb_9 = tce.utf16to8(this.content).getBytes();
		view.setInt32(pos,_sb_9.length);
		pos+=4;
		var _sb_10 = new Uint8Array(view.buffer);
		_sb_10.set(_sb_9,pos);
		pos += _sb_9.length;
		return pos;
	}	;	
	
	this.unmarshall = function(view,pos){
		var _sb_1 = view.getUint32(pos);
		pos+=4;
		this.seq = view.buffer.slice(pos,pos+_sb_1);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_1;
		this.seq = String.fromCharCode.apply(null, this.seq.getBytes());
		this.seq = tce.utf8to16(this.seq);
		var _sb_3 = view.getUint32(pos);
		pos+=4;
		this.sender_id = view.buffer.slice(pos,pos+_sb_3);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_3;
		this.sender_id = String.fromCharCode.apply(null, this.sender_id.getBytes());
		this.sender_id = tce.utf8to16(this.sender_id);
		var _sb_5 = view.getUint32(pos);
		pos+=4;
		this.send_time = view.buffer.slice(pos,pos+_sb_5);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_5;
		this.send_time = String.fromCharCode.apply(null, this.send_time.getBytes());
		this.send_time = tce.utf8to16(this.send_time);
		var _sb_7 = view.getUint32(pos);
		pos+=4;
		this.title = view.buffer.slice(pos,pos+_sb_7);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_7;
		this.title = String.fromCharCode.apply(null, this.title.getBytes());
		this.title = tce.utf8to16(this.title);
		var _sb_9 = view.getUint32(pos);
		pos+=4;
		this.content = view.buffer.slice(pos,pos+_sb_9);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_9;
		this.content = String.fromCharCode.apply(null, this.content.getBytes());
		this.content = tce.utf8to16(this.content);
		return pos;
	}	;	
	 // --  end function -- 
	
}




function Message_t(){
// -- STRUCT -- 
	this.seq = ''; 
	this.sender_id = ''; 
	this.sent_time = ''; 
	this.title = ''; 
	this.content = ''; 
	this.expire_time = ''; 
	this.send_time = ''; 
	this.accept_time = ''; 
	this.type = 0; 
	this.style = new MessageStyle_t(); 
	this.action = new ClickAction_t(); 
	this.custom = ''; 
	this.loop_times = 0; 
	this.loop_inerval = 0; 
	this.alert = ''; 
	this.badge = 0; 
	this.sound = ''; 
	this.category = ''; 
	this.raw = ''; 
	
	this.getsize = function(){
		var size =0;
		var _sb_1 = tce.utf16to8(this.seq);
		size+= 4 + _sb_1.getBytes().length;
		var _sb_2 = tce.utf16to8(this.sender_id);
		size+= 4 + _sb_2.getBytes().length;
		var _sb_3 = tce.utf16to8(this.sent_time);
		size+= 4 + _sb_3.getBytes().length;
		var _sb_4 = tce.utf16to8(this.title);
		size+= 4 + _sb_4.getBytes().length;
		var _sb_5 = tce.utf16to8(this.content);
		size+= 4 + _sb_5.getBytes().length;
		var _sb_6 = tce.utf16to8(this.expire_time);
		size+= 4 + _sb_6.getBytes().length;
		var _sb_7 = tce.utf16to8(this.send_time);
		size+= 4 + _sb_7.getBytes().length;
		var _sb_8 = tce.utf16to8(this.accept_time);
		size+= 4 + _sb_8.getBytes().length;
		size+= 4;
		size+=this.style.getsize();
		size+=this.action.getsize();
		var _sb_9 = tce.utf16to8(this.custom);
		size+= 4 + _sb_9.getBytes().length;
		size+= 4;
		size+= 4;
		var _sb_10 = tce.utf16to8(this.alert);
		size+= 4 + _sb_10.getBytes().length;
		size+= 4;
		var _sb_11 = tce.utf16to8(this.sound);
		size+= 4 + _sb_11.getBytes().length;
		var _sb_12 = tce.utf16to8(this.category);
		size+= 4 + _sb_12.getBytes().length;
		var _sb_13 = tce.utf16to8(this.raw);
		size+= 4 + _sb_13.getBytes().length;
		return size;
	}	;	
	
	// 
	this.marshall = function(view,pos){
		var _sb_1 = tce.utf16to8(this.seq).getBytes();
		view.setInt32(pos,_sb_1.length);
		pos+=4;
		var _sb_2 = new Uint8Array(view.buffer);
		_sb_2.set(_sb_1,pos);
		pos += _sb_1.length;
		var _sb_3 = tce.utf16to8(this.sender_id).getBytes();
		view.setInt32(pos,_sb_3.length);
		pos+=4;
		var _sb_4 = new Uint8Array(view.buffer);
		_sb_4.set(_sb_3,pos);
		pos += _sb_3.length;
		var _sb_5 = tce.utf16to8(this.sent_time).getBytes();
		view.setInt32(pos,_sb_5.length);
		pos+=4;
		var _sb_6 = new Uint8Array(view.buffer);
		_sb_6.set(_sb_5,pos);
		pos += _sb_5.length;
		var _sb_7 = tce.utf16to8(this.title).getBytes();
		view.setInt32(pos,_sb_7.length);
		pos+=4;
		var _sb_8 = new Uint8Array(view.buffer);
		_sb_8.set(_sb_7,pos);
		pos += _sb_7.length;
		var _sb_9 = tce.utf16to8(this.content).getBytes();
		view.setInt32(pos,_sb_9.length);
		pos+=4;
		var _sb_10 = new Uint8Array(view.buffer);
		_sb_10.set(_sb_9,pos);
		pos += _sb_9.length;
		var _sb_11 = tce.utf16to8(this.expire_time).getBytes();
		view.setInt32(pos,_sb_11.length);
		pos+=4;
		var _sb_12 = new Uint8Array(view.buffer);
		_sb_12.set(_sb_11,pos);
		pos += _sb_11.length;
		var _sb_13 = tce.utf16to8(this.send_time).getBytes();
		view.setInt32(pos,_sb_13.length);
		pos+=4;
		var _sb_14 = new Uint8Array(view.buffer);
		_sb_14.set(_sb_13,pos);
		pos += _sb_13.length;
		var _sb_15 = tce.utf16to8(this.accept_time).getBytes();
		view.setInt32(pos,_sb_15.length);
		pos+=4;
		var _sb_16 = new Uint8Array(view.buffer);
		_sb_16.set(_sb_15,pos);
		pos += _sb_15.length;
		view.setInt32(pos,this.type);
		pos+=4;
		pos= this.style.marshall(view,pos);
		pos= this.action.marshall(view,pos);
		var _sb_17 = tce.utf16to8(this.custom).getBytes();
		view.setInt32(pos,_sb_17.length);
		pos+=4;
		var _sb_18 = new Uint8Array(view.buffer);
		_sb_18.set(_sb_17,pos);
		pos += _sb_17.length;
		view.setInt32(pos,this.loop_times);
		pos+=4;
		view.setInt32(pos,this.loop_inerval);
		pos+=4;
		var _sb_19 = tce.utf16to8(this.alert).getBytes();
		view.setInt32(pos,_sb_19.length);
		pos+=4;
		var _sb_20 = new Uint8Array(view.buffer);
		_sb_20.set(_sb_19,pos);
		pos += _sb_19.length;
		view.setInt32(pos,this.badge);
		pos+=4;
		var _sb_21 = tce.utf16to8(this.sound).getBytes();
		view.setInt32(pos,_sb_21.length);
		pos+=4;
		var _sb_22 = new Uint8Array(view.buffer);
		_sb_22.set(_sb_21,pos);
		pos += _sb_21.length;
		var _sb_23 = tce.utf16to8(this.category).getBytes();
		view.setInt32(pos,_sb_23.length);
		pos+=4;
		var _sb_24 = new Uint8Array(view.buffer);
		_sb_24.set(_sb_23,pos);
		pos += _sb_23.length;
		var _sb_25 = tce.utf16to8(this.raw).getBytes();
		view.setInt32(pos,_sb_25.length);
		pos+=4;
		var _sb_26 = new Uint8Array(view.buffer);
		_sb_26.set(_sb_25,pos);
		pos += _sb_25.length;
		return pos;
	}	;	
	
	this.unmarshall = function(view,pos){
		var _sb_1 = view.getUint32(pos);
		pos+=4;
		this.seq = view.buffer.slice(pos,pos+_sb_1);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_1;
		this.seq = String.fromCharCode.apply(null, this.seq.getBytes());
		this.seq = tce.utf8to16(this.seq);
		var _sb_3 = view.getUint32(pos);
		pos+=4;
		this.sender_id = view.buffer.slice(pos,pos+_sb_3);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_3;
		this.sender_id = String.fromCharCode.apply(null, this.sender_id.getBytes());
		this.sender_id = tce.utf8to16(this.sender_id);
		var _sb_5 = view.getUint32(pos);
		pos+=4;
		this.sent_time = view.buffer.slice(pos,pos+_sb_5);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_5;
		this.sent_time = String.fromCharCode.apply(null, this.sent_time.getBytes());
		this.sent_time = tce.utf8to16(this.sent_time);
		var _sb_7 = view.getUint32(pos);
		pos+=4;
		this.title = view.buffer.slice(pos,pos+_sb_7);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_7;
		this.title = String.fromCharCode.apply(null, this.title.getBytes());
		this.title = tce.utf8to16(this.title);
		var _sb_9 = view.getUint32(pos);
		pos+=4;
		this.content = view.buffer.slice(pos,pos+_sb_9);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_9;
		this.content = String.fromCharCode.apply(null, this.content.getBytes());
		this.content = tce.utf8to16(this.content);
		var _sb_11 = view.getUint32(pos);
		pos+=4;
		this.expire_time = view.buffer.slice(pos,pos+_sb_11);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_11;
		this.expire_time = String.fromCharCode.apply(null, this.expire_time.getBytes());
		this.expire_time = tce.utf8to16(this.expire_time);
		var _sb_13 = view.getUint32(pos);
		pos+=4;
		this.send_time = view.buffer.slice(pos,pos+_sb_13);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_13;
		this.send_time = String.fromCharCode.apply(null, this.send_time.getBytes());
		this.send_time = tce.utf8to16(this.send_time);
		var _sb_15 = view.getUint32(pos);
		pos+=4;
		this.accept_time = view.buffer.slice(pos,pos+_sb_15);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_15;
		this.accept_time = String.fromCharCode.apply(null, this.accept_time.getBytes());
		this.accept_time = tce.utf8to16(this.accept_time);
		this.type = view.getInt32(pos);
		pos+=4;
		pos = this.style.unmarshall(view,pos);
		pos = this.action.unmarshall(view,pos);
		var _sb_17 = view.getUint32(pos);
		pos+=4;
		this.custom = view.buffer.slice(pos,pos+_sb_17);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_17;
		this.custom = String.fromCharCode.apply(null, this.custom.getBytes());
		this.custom = tce.utf8to16(this.custom);
		this.loop_times = view.getInt32(pos);
		pos+=4;
		this.loop_inerval = view.getInt32(pos);
		pos+=4;
		var _sb_19 = view.getUint32(pos);
		pos+=4;
		this.alert = view.buffer.slice(pos,pos+_sb_19);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_19;
		this.alert = String.fromCharCode.apply(null, this.alert.getBytes());
		this.alert = tce.utf8to16(this.alert);
		this.badge = view.getInt32(pos);
		pos+=4;
		var _sb_21 = view.getUint32(pos);
		pos+=4;
		this.sound = view.buffer.slice(pos,pos+_sb_21);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_21;
		this.sound = String.fromCharCode.apply(null, this.sound.getBytes());
		this.sound = tce.utf8to16(this.sound);
		var _sb_23 = view.getUint32(pos);
		pos+=4;
		this.category = view.buffer.slice(pos,pos+_sb_23);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_23;
		this.category = String.fromCharCode.apply(null, this.category.getBytes());
		this.category = tce.utf8to16(this.category);
		var _sb_25 = view.getUint32(pos);
		pos+=4;
		this.raw = view.buffer.slice(pos,pos+_sb_25);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_25;
		this.raw = String.fromCharCode.apply(null, this.raw.getBytes());
		this.raw = tce.utf8to16(this.raw);
		return pos;
	}	;	
	 // --  end function -- 
	
}




function Notification_t(){
// -- STRUCT -- 
	this.type = ''; 
	this.title = ''; 
	this.content = ''; 
	this.p1 = ''; 
	this.p2 = ''; 
	
	this.getsize = function(){
		var size =0;
		var _sb_1 = tce.utf16to8(this.type);
		size+= 4 + _sb_1.getBytes().length;
		var _sb_2 = tce.utf16to8(this.title);
		size+= 4 + _sb_2.getBytes().length;
		var _sb_3 = tce.utf16to8(this.content);
		size+= 4 + _sb_3.getBytes().length;
		var _sb_4 = tce.utf16to8(this.p1);
		size+= 4 + _sb_4.getBytes().length;
		var _sb_5 = tce.utf16to8(this.p2);
		size+= 4 + _sb_5.getBytes().length;
		return size;
	}	;	
	
	// 
	this.marshall = function(view,pos){
		var _sb_1 = tce.utf16to8(this.type).getBytes();
		view.setInt32(pos,_sb_1.length);
		pos+=4;
		var _sb_2 = new Uint8Array(view.buffer);
		_sb_2.set(_sb_1,pos);
		pos += _sb_1.length;
		var _sb_3 = tce.utf16to8(this.title).getBytes();
		view.setInt32(pos,_sb_3.length);
		pos+=4;
		var _sb_4 = new Uint8Array(view.buffer);
		_sb_4.set(_sb_3,pos);
		pos += _sb_3.length;
		var _sb_5 = tce.utf16to8(this.content).getBytes();
		view.setInt32(pos,_sb_5.length);
		pos+=4;
		var _sb_6 = new Uint8Array(view.buffer);
		_sb_6.set(_sb_5,pos);
		pos += _sb_5.length;
		var _sb_7 = tce.utf16to8(this.p1).getBytes();
		view.setInt32(pos,_sb_7.length);
		pos+=4;
		var _sb_8 = new Uint8Array(view.buffer);
		_sb_8.set(_sb_7,pos);
		pos += _sb_7.length;
		var _sb_9 = tce.utf16to8(this.p2).getBytes();
		view.setInt32(pos,_sb_9.length);
		pos+=4;
		var _sb_10 = new Uint8Array(view.buffer);
		_sb_10.set(_sb_9,pos);
		pos += _sb_9.length;
		return pos;
	}	;	
	
	this.unmarshall = function(view,pos){
		var _sb_1 = view.getUint32(pos);
		pos+=4;
		this.type = view.buffer.slice(pos,pos+_sb_1);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_1;
		this.type = String.fromCharCode.apply(null, this.type.getBytes());
		this.type = tce.utf8to16(this.type);
		var _sb_3 = view.getUint32(pos);
		pos+=4;
		this.title = view.buffer.slice(pos,pos+_sb_3);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_3;
		this.title = String.fromCharCode.apply(null, this.title.getBytes());
		this.title = tce.utf8to16(this.title);
		var _sb_5 = view.getUint32(pos);
		pos+=4;
		this.content = view.buffer.slice(pos,pos+_sb_5);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_5;
		this.content = String.fromCharCode.apply(null, this.content.getBytes());
		this.content = tce.utf8to16(this.content);
		var _sb_7 = view.getUint32(pos);
		pos+=4;
		this.p1 = view.buffer.slice(pos,pos+_sb_7);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_7;
		this.p1 = String.fromCharCode.apply(null, this.p1.getBytes());
		this.p1 = tce.utf8to16(this.p1);
		var _sb_9 = view.getUint32(pos);
		pos+=4;
		this.p2 = view.buffer.slice(pos,pos+_sb_9);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_9;
		this.p2 = String.fromCharCode.apply(null, this.p2.getBytes());
		this.p2 = tce.utf8to16(this.p2);
		return pos;
	}	;	
	 // --  end function -- 
	
}



function ITerminalProxy(){
	this.conn = null;
	this.delta =null;
	
	this.destroy = function(){
		try{
			this.conn.close();
		}catch(e){
			tce.RpcCommunicator.instance().getLogger().error(e.toString());
		}		
	}	;	
	
	this.onSimpleText_oneway = function (text,error,props){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ONEWAY);
		m.ifidx = 0;
		m.opidx = 0;
		m.paramsize = 1;
		error = arguments[1]?arguments[1]:null;
		m.onerror = error;
		props = arguments[2]?arguments[2]:null;
		m.extra=props;
		try{
			var size =0;
			size+=text.getsize();
			var _bf_11 = new ArrayBuffer(size);
			var _view = new DataView(_bf_11);
			var _pos=0;
			_pos = text.marshall(_view,_pos);
			m.paramstream =_bf_11;
			m.prx = this;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "RPCERROR_SENDFAILED";
		}		
	}	;	
	
	this.onSimpleText_async = function(text,async,error,props,cookie){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ASYNC);
		m.ifidx		= 0;
		m.opidx		= 0;
		error		= arguments[2]?arguments[2]:null;
		m.onerror	= error;
		props		= arguments[3]?arguments[3]:null;
		m.extra		= props;
		cookie 		= arguments[4]?arguments[4]:null;
		m.cookie	= cookie;
		m.extra		= props;
		m.paramsize = 1;
		try{
			var size =0;
			size += text.getsize();
			var _bf_1 = new ArrayBuffer(size);
			var _view = new DataView(_bf_1);
			var _pos=0;
			_pos+=text.marshall(_view,_pos);
			m.paramstream =_bf_1;
			m.prx = this;
			m.async = async;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "tce.RpcConsts.RPCERROR_SENDFAILED";
		}		
	}	;	
	
	
	this.onMessage_oneway = function (message,error,props){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ONEWAY);
		m.ifidx = 0;
		m.opidx = 1;
		m.paramsize = 1;
		error = arguments[1]?arguments[1]:null;
		m.onerror = error;
		props = arguments[2]?arguments[2]:null;
		m.extra=props;
		try{
			var size =0;
			size+=message.getsize();
			var _bf_2 = new ArrayBuffer(size);
			var _view = new DataView(_bf_2);
			var _pos=0;
			_pos = message.marshall(_view,_pos);
			m.paramstream =_bf_2;
			m.prx = this;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "RPCERROR_SENDFAILED";
		}		
	}	;	
	
	this.onMessage_async = function(message,async,error,props,cookie){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ASYNC);
		m.ifidx		= 0;
		m.opidx		= 1;
		error		= arguments[2]?arguments[2]:null;
		m.onerror	= error;
		props		= arguments[3]?arguments[3]:null;
		m.extra		= props;
		cookie 		= arguments[4]?arguments[4]:null;
		m.cookie	= cookie;
		m.extra		= props;
		m.paramsize = 1;
		try{
			var size =0;
			size += message.getsize();
			var _bf_1 = new ArrayBuffer(size);
			var _view = new DataView(_bf_1);
			var _pos=0;
			_pos+=message.marshall(_view,_pos);
			m.paramstream =_bf_1;
			m.prx = this;
			m.async = async;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "tce.RpcConsts.RPCERROR_SENDFAILED";
		}		
	}	;	
	
	
	this.onError_oneway = function (errcode,errmsg,error,props){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ONEWAY);
		m.ifidx = 0;
		m.opidx = 2;
		m.paramsize = 2;
		error = arguments[2]?arguments[2]:null;
		m.onerror = error;
		props = arguments[3]?arguments[3]:null;
		m.extra=props;
		try{
			var size =0;
			var _sb_2 = tce.utf16to8(errcode);
			size+= 4 + _sb_2.getBytes().length;
			var _sb_3 = tce.utf16to8(errmsg);
			size+= 4 + _sb_3.getBytes().length;
			var _bf_4 = new ArrayBuffer(size);
			var _view = new DataView(_bf_4);
			var _pos=0;
			var _sb_5 = tce.utf16to8(errcode).getBytes();
			_view.setInt32(_pos,_sb_5.length);
			_pos+=4;
			var _sb_6 = new Uint8Array(_view.buffer);
			_sb_6.set(_sb_5,_pos);
			_pos += _sb_5.length;
			var _sb_7 = tce.utf16to8(errmsg).getBytes();
			_view.setInt32(_pos,_sb_7.length);
			_pos+=4;
			var _sb_8 = new Uint8Array(_view.buffer);
			_sb_8.set(_sb_7,_pos);
			_pos += _sb_7.length;
			m.paramstream =_bf_4;
			m.prx = this;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "RPCERROR_SENDFAILED";
		}		
	}	;	
	
	this.onError_async = function(errcode,errmsg,async,error,props,cookie){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ASYNC);
		m.ifidx		= 0;
		m.opidx		= 2;
		error		= arguments[3]?arguments[3]:null;
		m.onerror	= error;
		props		= arguments[4]?arguments[4]:null;
		m.extra		= props;
		cookie 		= arguments[5]?arguments[5]:null;
		m.cookie	= cookie;
		m.extra		= props;
		m.paramsize = 2;
		try{
			var size =0;
			var _sb_1 = tce.utf16to8(errcode);
			size+= 4 + _sb_1.getBytes().length;
			var _sb_2 = tce.utf16to8(errmsg);
			size+= 4 + _sb_2.getBytes().length;
			var _bf_3 = new ArrayBuffer(size);
			var _view = new DataView(_bf_3);
			var _pos=0;
			var _sb_4 = tce.utf16to8(errcode).getBytes();
			_view.setInt32(_pos,_sb_4.length);
			_pos+=4;
			var _sb_5 = new Uint8Array(_view.buffer);
			_sb_5.set(_sb_4,_pos);
			_pos += _sb_4.length;
			var _sb_6 = tce.utf16to8(errmsg).getBytes();
			_view.setInt32(_pos,_sb_6.length);
			_pos+=4;
			var _sb_7 = new Uint8Array(_view.buffer);
			_sb_7.set(_sb_6,_pos);
			_pos += _sb_6.length;
			m.paramstream =_bf_3;
			m.prx = this;
			m.async = async;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "tce.RpcConsts.RPCERROR_SENDFAILED";
		}		
	}	;	
	
	
	this.onSystemNotification_oneway = function (notification,error,props){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ONEWAY);
		m.ifidx = 0;
		m.opidx = 3;
		m.paramsize = 1;
		error = arguments[1]?arguments[1]:null;
		m.onerror = error;
		props = arguments[2]?arguments[2]:null;
		m.extra=props;
		try{
			var size =0;
			size+=notification.getsize();
			var _bf_8 = new ArrayBuffer(size);
			var _view = new DataView(_bf_8);
			var _pos=0;
			_pos = notification.marshall(_view,_pos);
			m.paramstream =_bf_8;
			m.prx = this;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "RPCERROR_SENDFAILED";
		}		
	}	;	
	
	this.onSystemNotification_async = function(notification,async,error,props,cookie){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ASYNC);
		m.ifidx		= 0;
		m.opidx		= 3;
		error		= arguments[2]?arguments[2]:null;
		m.onerror	= error;
		props		= arguments[3]?arguments[3]:null;
		m.extra		= props;
		cookie 		= arguments[4]?arguments[4]:null;
		m.cookie	= cookie;
		m.extra		= props;
		m.paramsize = 1;
		try{
			var size =0;
			size += notification.getsize();
			var _bf_1 = new ArrayBuffer(size);
			var _view = new DataView(_bf_1);
			var _pos=0;
			_pos+=notification.marshall(_view,_pos);
			m.paramstream =_bf_1;
			m.prx = this;
			m.async = async;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "tce.RpcConsts.RPCERROR_SENDFAILED";
		}		
	}	;	
	
	
	this.AsyncCallBack = function(m1,m2){
		var array = new Uint8Array(m2.paramstream);
		var view = new DataView(array.buffer);
		var pos=0;
		if(m1.opidx == 0){
			m1.async(m1.prx,m1.cookie);
		}		
		if(m1.opidx == 1){
			m1.async(m1.prx,m1.cookie);
		}		
		if(m1.opidx == 2){
			m1.async(m1.prx,m1.cookie);
		}		
		if(m1.opidx == 3){
			m1.async(m1.prx,m1.cookie);
		}		
	}	;	
	
}
ITerminalProxy.create = function(uri){
	var prx = new ITerminalProxy();
	prx.conn = new tce.RpcConnection(uri);
	return prx;
};

ITerminalProxy.createWithProxy = function(proxy){
	var prx = new ITerminalProxy();
	prx.conn = proxy.conn;
	return prx;
};


// class ITerminal
function ITerminal(){
	//# -- INTERFACE -- 
	this.delegate = new ITerminal_delegate(this);
	
	//public  onSimpleText(text,tce.RpcContext ctx){
	this.onSimpleText = function(text,ctx){
	}	
	
	//public  onMessage(message,tce.RpcContext ctx){
	this.onMessage = function(message,ctx){
	}	
	
	//public  onError(errcode,errmsg,tce.RpcContext ctx){
	this.onError = function(errcode,errmsg,ctx){
	}	
	
	//public  onSystemNotification(notification,tce.RpcContext ctx){
	this.onSystemNotification = function(notification,ctx){
	}	
}

function ITerminal_delegate(inst) {
	
	this.inst = inst;
	this.ifidx = 0;
	this.invoke = function(m){
		if(m.opidx == 0 ){
			return this.func_0_delegate(m);
		}		
		if(m.opidx == 1 ){
			return this.func_1_delegate(m);
		}		
		if(m.opidx == 2 ){
			return this.func_2_delegate(m);
		}		
		if(m.opidx == 3 ){
			return this.func_3_delegate(m);
		}		
		return false;
	}	;	
	
	this.func_0_delegate = function(m){
		var r = false;
		var pos =0;
		var array = null;
		var view = null;
		array = new Uint8Array(m.paramstream);
		view = new DataView(array.buffer);
		var text = new SimpleText_t();
		pos= text.unmarshall(view,pos);
		var servant = this.inst;
		var ctx = new tce.RpcContext();
		ctx.msg = m;
		servant.onSimpleText(text,ctx);
		if( (m.calltype & tce.RpcMessage.ONEWAY) !=0 ){
			return true;
		}		
		
		return r;
	}	;	
	
	this.func_1_delegate = function(m){
		var r = false;
		var pos =0;
		var array = null;
		var view = null;
		array = new Uint8Array(m.paramstream);
		view = new DataView(array.buffer);
		var message = new Message_t();
		pos= message.unmarshall(view,pos);
		var servant = this.inst;
		var ctx = new tce.RpcContext();
		ctx.msg = m;
		servant.onMessage(message,ctx);
		if( (m.calltype & tce.RpcMessage.ONEWAY) !=0 ){
			return true;
		}		
		
		return r;
	}	;	
	
	this.func_2_delegate = function(m){
		var r = false;
		var pos =0;
		var array = null;
		var view = null;
		array = new Uint8Array(m.paramstream);
		view = new DataView(array.buffer);
		var errcode;
		var _sb_6 = view.getUint32(pos);
		pos+=4;
		errcode = view.buffer.slice(pos,pos+_sb_6);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_6;
		errcode = String.fromCharCode.apply(null, errcode.getBytes());
		errcode = tce.utf8to16(errcode);
		var errmsg;
		var _sb_8 = view.getUint32(pos);
		pos+=4;
		errmsg = view.buffer.slice(pos,pos+_sb_8);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_8;
		errmsg = String.fromCharCode.apply(null, errmsg.getBytes());
		errmsg = tce.utf8to16(errmsg);
		var servant = this.inst;
		var ctx = new tce.RpcContext();
		ctx.msg = m;
		servant.onError(errcode,errmsg,ctx);
		if( (m.calltype & tce.RpcMessage.ONEWAY) !=0 ){
			return true;
		}		
		
		return r;
	}	;	
	
	this.func_3_delegate = function(m){
		var r = false;
		var pos =0;
		var array = null;
		var view = null;
		array = new Uint8Array(m.paramstream);
		view = new DataView(array.buffer);
		var notification = new Notification_t();
		pos= notification.unmarshall(view,pos);
		var servant = this.inst;
		var ctx = new tce.RpcContext();
		ctx.msg = m;
		servant.onSystemNotification(notification,ctx);
		if( (m.calltype & tce.RpcMessage.ONEWAY) !=0 ){
			return true;
		}		
		
		return r;
	}	;	
	
}


function IUserEventListenerProxy(){
	this.conn = null;
	this.delta =null;
	
	this.destroy = function(){
		try{
			this.conn.close();
		}catch(e){
			tce.RpcCommunicator.instance().getLogger().error(e.toString());
		}		
	}	;	
	
	this.onUserOnline_oneway = function (userid,gws_id,device,error,props){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ONEWAY);
		m.ifidx = 1;
		m.opidx = 0;
		m.paramsize = 3;
		error = arguments[3]?arguments[3]:null;
		m.onerror = error;
		props = arguments[4]?arguments[4]:null;
		m.extra=props;
		try{
			var size =0;
			var _sb_10 = tce.utf16to8(userid);
			size+= 4 + _sb_10.getBytes().length;
			var _sb_11 = tce.utf16to8(gws_id);
			size+= 4 + _sb_11.getBytes().length;
			size+= 4;
			var _bf_12 = new ArrayBuffer(size);
			var _view = new DataView(_bf_12);
			var _pos=0;
			var _sb_13 = tce.utf16to8(userid).getBytes();
			_view.setInt32(_pos,_sb_13.length);
			_pos+=4;
			var _sb_14 = new Uint8Array(_view.buffer);
			_sb_14.set(_sb_13,_pos);
			_pos += _sb_13.length;
			var _sb_15 = tce.utf16to8(gws_id).getBytes();
			_view.setInt32(_pos,_sb_15.length);
			_pos+=4;
			var _sb_16 = new Uint8Array(_view.buffer);
			_sb_16.set(_sb_15,_pos);
			_pos += _sb_15.length;
			_view.setInt32(_pos,device);
			_pos+=4;
			m.paramstream =_bf_12;
			m.prx = this;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "RPCERROR_SENDFAILED";
		}		
	}	;	
	
	this.onUserOnline_async = function(userid,gws_id,device,async,error,props,cookie){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ASYNC);
		m.ifidx		= 1;
		m.opidx		= 0;
		error		= arguments[4]?arguments[4]:null;
		m.onerror	= error;
		props		= arguments[5]?arguments[5]:null;
		m.extra		= props;
		cookie 		= arguments[6]?arguments[6]:null;
		m.cookie	= cookie;
		m.extra		= props;
		m.paramsize = 3;
		try{
			var size =0;
			var _sb_1 = tce.utf16to8(userid);
			size+= 4 + _sb_1.getBytes().length;
			var _sb_2 = tce.utf16to8(gws_id);
			size+= 4 + _sb_2.getBytes().length;
			size+= 4;
			var _bf_3 = new ArrayBuffer(size);
			var _view = new DataView(_bf_3);
			var _pos=0;
			var _sb_4 = tce.utf16to8(userid).getBytes();
			_view.setInt32(_pos,_sb_4.length);
			_pos+=4;
			var _sb_5 = new Uint8Array(_view.buffer);
			_sb_5.set(_sb_4,_pos);
			_pos += _sb_4.length;
			var _sb_6 = tce.utf16to8(gws_id).getBytes();
			_view.setInt32(_pos,_sb_6.length);
			_pos+=4;
			var _sb_7 = new Uint8Array(_view.buffer);
			_sb_7.set(_sb_6,_pos);
			_pos += _sb_6.length;
			_view.setInt32(_pos,device);
			_pos+=4;
			m.paramstream =_bf_3;
			m.prx = this;
			m.async = async;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "tce.RpcConsts.RPCERROR_SENDFAILED";
		}		
	}	;	
	
	
	this.onUserOffline_oneway = function (userid,gws_id,device,error,props){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ONEWAY);
		m.ifidx = 1;
		m.opidx = 1;
		m.paramsize = 3;
		error = arguments[3]?arguments[3]:null;
		m.onerror = error;
		props = arguments[4]?arguments[4]:null;
		m.extra=props;
		try{
			var size =0;
			var _sb_8 = tce.utf16to8(userid);
			size+= 4 + _sb_8.getBytes().length;
			var _sb_9 = tce.utf16to8(gws_id);
			size+= 4 + _sb_9.getBytes().length;
			size+= 4;
			var _bf_10 = new ArrayBuffer(size);
			var _view = new DataView(_bf_10);
			var _pos=0;
			var _sb_11 = tce.utf16to8(userid).getBytes();
			_view.setInt32(_pos,_sb_11.length);
			_pos+=4;
			var _sb_12 = new Uint8Array(_view.buffer);
			_sb_12.set(_sb_11,_pos);
			_pos += _sb_11.length;
			var _sb_13 = tce.utf16to8(gws_id).getBytes();
			_view.setInt32(_pos,_sb_13.length);
			_pos+=4;
			var _sb_14 = new Uint8Array(_view.buffer);
			_sb_14.set(_sb_13,_pos);
			_pos += _sb_13.length;
			_view.setInt32(_pos,device);
			_pos+=4;
			m.paramstream =_bf_10;
			m.prx = this;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "RPCERROR_SENDFAILED";
		}		
	}	;	
	
	this.onUserOffline_async = function(userid,gws_id,device,async,error,props,cookie){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ASYNC);
		m.ifidx		= 1;
		m.opidx		= 1;
		error		= arguments[4]?arguments[4]:null;
		m.onerror	= error;
		props		= arguments[5]?arguments[5]:null;
		m.extra		= props;
		cookie 		= arguments[6]?arguments[6]:null;
		m.cookie	= cookie;
		m.extra		= props;
		m.paramsize = 3;
		try{
			var size =0;
			var _sb_1 = tce.utf16to8(userid);
			size+= 4 + _sb_1.getBytes().length;
			var _sb_2 = tce.utf16to8(gws_id);
			size+= 4 + _sb_2.getBytes().length;
			size+= 4;
			var _bf_3 = new ArrayBuffer(size);
			var _view = new DataView(_bf_3);
			var _pos=0;
			var _sb_4 = tce.utf16to8(userid).getBytes();
			_view.setInt32(_pos,_sb_4.length);
			_pos+=4;
			var _sb_5 = new Uint8Array(_view.buffer);
			_sb_5.set(_sb_4,_pos);
			_pos += _sb_4.length;
			var _sb_6 = tce.utf16to8(gws_id).getBytes();
			_view.setInt32(_pos,_sb_6.length);
			_pos+=4;
			var _sb_7 = new Uint8Array(_view.buffer);
			_sb_7.set(_sb_6,_pos);
			_pos += _sb_6.length;
			_view.setInt32(_pos,device);
			_pos+=4;
			m.paramstream =_bf_3;
			m.prx = this;
			m.async = async;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "tce.RpcConsts.RPCERROR_SENDFAILED";
		}		
	}	;	
	
	
	this.AsyncCallBack = function(m1,m2){
		var array = new Uint8Array(m2.paramstream);
		var view = new DataView(array.buffer);
		var pos=0;
		if(m1.opidx == 0){
			m1.async(m1.prx,m1.cookie);
		}		
		if(m1.opidx == 1){
			m1.async(m1.prx,m1.cookie);
		}		
	}	;	
	
}
IUserEventListenerProxy.create = function(uri){
	var prx = new IUserEventListenerProxy();
	prx.conn = new tce.RpcConnection(uri);
	return prx;
};

IUserEventListenerProxy.createWithProxy = function(proxy){
	var prx = new IUserEventListenerProxy();
	prx.conn = proxy.conn;
	return prx;
};


// class IUserEventListener
function IUserEventListener(){
	//# -- INTERFACE -- 
	this.delegate = new IUserEventListener_delegate(this);
	
	//public  onUserOnline(userid,gws_id,device,tce.RpcContext ctx){
	this.onUserOnline = function(userid,gws_id,device,ctx){
	}	
	
	//public  onUserOffline(userid,gws_id,device,tce.RpcContext ctx){
	this.onUserOffline = function(userid,gws_id,device,ctx){
	}	
}

function IUserEventListener_delegate(inst) {
	
	this.inst = inst;
	this.ifidx = 1;
	this.invoke = function(m){
		if(m.opidx == 0 ){
			return this.func_0_delegate(m);
		}		
		if(m.opidx == 1 ){
			return this.func_1_delegate(m);
		}		
		return false;
	}	;	
	
	this.func_0_delegate = function(m){
		var r = false;
		var pos =0;
		var array = null;
		var view = null;
		array = new Uint8Array(m.paramstream);
		view = new DataView(array.buffer);
		var userid;
		var _sb_10 = view.getUint32(pos);
		pos+=4;
		userid = view.buffer.slice(pos,pos+_sb_10);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_10;
		userid = String.fromCharCode.apply(null, userid.getBytes());
		userid = tce.utf8to16(userid);
		var gws_id;
		var _sb_12 = view.getUint32(pos);
		pos+=4;
		gws_id = view.buffer.slice(pos,pos+_sb_12);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_12;
		gws_id = String.fromCharCode.apply(null, gws_id.getBytes());
		gws_id = tce.utf8to16(gws_id);
		var device;
		device = view.getInt32(pos);
		pos+=4;
		var servant = this.inst;
		var ctx = new tce.RpcContext();
		ctx.msg = m;
		servant.onUserOnline(userid,gws_id,device,ctx);
		if( (m.calltype & tce.RpcMessage.ONEWAY) !=0 ){
			return true;
		}		
		
		return r;
	}	;	
	
	this.func_1_delegate = function(m){
		var r = false;
		var pos =0;
		var array = null;
		var view = null;
		array = new Uint8Array(m.paramstream);
		view = new DataView(array.buffer);
		var userid;
		var _sb_14 = view.getUint32(pos);
		pos+=4;
		userid = view.buffer.slice(pos,pos+_sb_14);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_14;
		userid = String.fromCharCode.apply(null, userid.getBytes());
		userid = tce.utf8to16(userid);
		var gws_id;
		var _sb_16 = view.getUint32(pos);
		pos+=4;
		gws_id = view.buffer.slice(pos,pos+_sb_16);
		// this var is Uint8Array,should convert to String!!
		pos+= _sb_16;
		gws_id = String.fromCharCode.apply(null, gws_id.getBytes());
		gws_id = tce.utf8to16(gws_id);
		var device;
		device = view.getInt32(pos);
		pos+=4;
		var servant = this.inst;
		var ctx = new tce.RpcContext();
		ctx.msg = m;
		servant.onUserOffline(userid,gws_id,device,ctx);
		if( (m.calltype & tce.RpcMessage.ONEWAY) !=0 ){
			return true;
		}		
		
		return r;
	}	;	
	
}


function ITerminalGatewayServerProxy(){
	this.conn = null;
	this.delta =null;
	
	this.destroy = function(){
		try{
			this.conn.close();
		}catch(e){
			tce.RpcCommunicator.instance().getLogger().error(e.toString());
		}		
	}	;	
	
	this.ping_oneway = function (error,props){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ONEWAY);
		m.ifidx = 2;
		m.opidx = 0;
		m.paramsize = 0;
		error = arguments[0]?arguments[0]:null;
		m.onerror = error;
		props = arguments[1]?arguments[1]:null;
		m.extra=props;
		try{
			var size =0;
			var _bf_18 = new ArrayBuffer(size);
			var _view = new DataView(_bf_18);
			var _pos=0;
			m.prx = this;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "RPCERROR_SENDFAILED";
		}		
	}	;	
	
	this.ping_async = function(async,error,props,cookie){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ASYNC);
		m.ifidx		= 2;
		m.opidx		= 0;
		error		= arguments[1]?arguments[1]:null;
		m.onerror	= error;
		props		= arguments[2]?arguments[2]:null;
		m.extra		= props;
		cookie 		= arguments[3]?arguments[3]:null;
		m.cookie	= cookie;
		m.extra		= props;
		m.paramsize = 0;
		try{
			var size =0;
			var _bf_1 = new ArrayBuffer(size);
			var _view = new DataView(_bf_1);
			var _pos=0;
			m.prx = this;
			m.async = async;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "tce.RpcConsts.RPCERROR_SENDFAILED";
		}		
	}	;	
	
	
	this.AsyncCallBack = function(m1,m2){
		var array = new Uint8Array(m2.paramstream);
		var view = new DataView(array.buffer);
		var pos=0;
		if(m1.opidx == 0){
			m1.async(m1.prx,m1.cookie);
		}		
	}	;	
	
}
ITerminalGatewayServerProxy.create = function(uri){
	var prx = new ITerminalGatewayServerProxy();
	prx.conn = new tce.RpcConnection(uri);
	return prx;
};

ITerminalGatewayServerProxy.createWithProxy = function(proxy){
	var prx = new ITerminalGatewayServerProxy();
	prx.conn = proxy.conn;
	return prx;
};


// class ITerminalGatewayServer
function ITerminalGatewayServer(){
	//# -- INTERFACE -- 
	this.delegate = new ITerminalGatewayServer_delegate(this);
	
	//public  ping(tce.RpcContext ctx){
	this.ping = function(ctx){
	}	
}

function ITerminalGatewayServer_delegate(inst) {
	
	this.inst = inst;
	this.ifidx = 2;
	this.invoke = function(m){
		if(m.opidx == 0 ){
			return this.func_0_delegate(m);
		}		
		return false;
	}	;	
	
	this.func_0_delegate = function(m){
		var r = false;
		var pos =0;
		var array = null;
		var view = null;
		var servant = this.inst;
		var ctx = new tce.RpcContext();
		ctx.msg = m;
		servant.ping(ctx);
		if( (m.calltype & tce.RpcMessage.ONEWAY) !=0 ){
			return true;
		}		
		
		return r;
	}	;	
	
}


function IMessageServerProxy(){
	this.conn = null;
	this.delta =null;
	
	this.destroy = function(){
		try{
			this.conn.close();
		}catch(e){
			tce.RpcCommunicator.instance().getLogger().error(e.toString());
		}		
	}	;	
	
	this.sendMessage_oneway = function (token_list,message,error,props){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ONEWAY);
		m.ifidx = 3;
		m.opidx = 0;
		m.paramsize = 2;
		error = arguments[2]?arguments[2]:null;
		m.onerror = error;
		props = arguments[3]?arguments[3]:null;
		m.extra=props;
		try{
			var size =0;
			var _c_3 = new SIDS_thlp(token_list);
			size+=_c_3.getsize();
			size+=message.getsize();
			var _bf_4 = new ArrayBuffer(size);
			var _view = new DataView(_bf_4);
			var _pos=0;
			var _c_5 = new SIDS_thlp(token_list);
			_pos = _c_5.marshall(_view,_pos);
			_pos = message.marshall(_view,_pos);
			m.paramstream =_bf_4;
			m.prx = this;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "RPCERROR_SENDFAILED";
		}		
	}	;	
	
	this.sendMessage_async = function(token_list,message,async,error,props,cookie){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ASYNC);
		m.ifidx		= 3;
		m.opidx		= 0;
		error		= arguments[3]?arguments[3]:null;
		m.onerror	= error;
		props		= arguments[4]?arguments[4]:null;
		m.extra		= props;
		cookie 		= arguments[5]?arguments[5]:null;
		m.cookie	= cookie;
		m.extra		= props;
		m.paramsize = 2;
		try{
			var size =0;
			var _c_1 = new SIDS_thlp(token_list);
			size += _c_1.getsize();
			size += message.getsize();
			var _bf_2 = new ArrayBuffer(size);
			var _view = new DataView(_bf_2);
			var _pos=0;
			var _c_3 = new SIDS_thlp(token_list);
			_pos+=_c_3.marshall(_view,_pos);
			_pos+=message.marshall(_view,_pos);
			m.paramstream =_bf_2;
			m.prx = this;
			m.async = async;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "tce.RpcConsts.RPCERROR_SENDFAILED";
		}		
	}	;	
	
	
	this.confirmMessage_oneway = function (seqs,error,props){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ONEWAY);
		m.ifidx = 3;
		m.opidx = 1;
		m.paramsize = 1;
		error = arguments[1]?arguments[1]:null;
		m.onerror = error;
		props = arguments[2]?arguments[2]:null;
		m.extra=props;
		try{
			var size =0;
			var _c_4 = new SIDS_thlp(seqs);
			size+=_c_4.getsize();
			var _bf_5 = new ArrayBuffer(size);
			var _view = new DataView(_bf_5);
			var _pos=0;
			var _c_6 = new SIDS_thlp(seqs);
			_pos = _c_6.marshall(_view,_pos);
			m.paramstream =_bf_5;
			m.prx = this;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "RPCERROR_SENDFAILED";
		}		
	}	;	
	
	this.confirmMessage_async = function(seqs,async,error,props,cookie){
		var r = false;
		var m = new tce.RpcMessage(tce.RpcMessage.CALL|tce.RpcMessage.ASYNC);
		m.ifidx		= 3;
		m.opidx		= 1;
		error		= arguments[2]?arguments[2]:null;
		m.onerror	= error;
		props		= arguments[3]?arguments[3]:null;
		m.extra		= props;
		cookie 		= arguments[4]?arguments[4]:null;
		m.cookie	= cookie;
		m.extra		= props;
		m.paramsize = 1;
		try{
			var size =0;
			var _c_1 = new SIDS_thlp(seqs);
			size += _c_1.getsize();
			var _bf_2 = new ArrayBuffer(size);
			var _view = new DataView(_bf_2);
			var _pos=0;
			var _c_3 = new SIDS_thlp(seqs);
			_pos+=_c_3.marshall(_view,_pos);
			m.paramstream =_bf_2;
			m.prx = this;
			m.async = async;
		}catch(e){
			console.log(e.toString());
			throw "RPCERROR_DATADIRTY";
		}		
		r = this.conn.sendMessage(m);
		if(!r){
			throw "tce.RpcConsts.RPCERROR_SENDFAILED";
		}		
	}	;	
	
	
	this.AsyncCallBack = function(m1,m2){
		var array = new Uint8Array(m2.paramstream);
		var view = new DataView(array.buffer);
		var pos=0;
		if(m1.opidx == 0){
			m1.async(m1.prx,m1.cookie);
		}		
		if(m1.opidx == 1){
			m1.async(m1.prx,m1.cookie);
		}		
	}	;	
	
}
IMessageServerProxy.create = function(uri){
	var prx = new IMessageServerProxy();
	prx.conn = new tce.RpcConnection(uri);
	return prx;
};

IMessageServerProxy.createWithProxy = function(proxy){
	var prx = new IMessageServerProxy();
	prx.conn = proxy.conn;
	return prx;
};


// class IMessageServer
function IMessageServer(){
	//# -- INTERFACE -- 
	this.delegate = new IMessageServer_delegate(this);
	
	//public  sendMessage(token_list,message,tce.RpcContext ctx){
	this.sendMessage = function(token_list,message,ctx){
	}	
	
	//public  confirmMessage(seqs,tce.RpcContext ctx){
	this.confirmMessage = function(seqs,ctx){
	}	
}

function IMessageServer_delegate(inst) {
	
	this.inst = inst;
	this.ifidx = 3;
	this.invoke = function(m){
		if(m.opidx == 0 ){
			return this.func_0_delegate(m);
		}		
		if(m.opidx == 1 ){
			return this.func_1_delegate(m);
		}		
		return false;
	}	;	
	
	this.func_0_delegate = function(m){
		var r = false;
		var pos =0;
		var array = null;
		var view = null;
		array = new Uint8Array(m.paramstream);
		view = new DataView(array.buffer);
		var token_list = [];
		var _array_6 = new SIDS_thlp(token_list);
		pos=_array_6.unmarshall(view,pos);
		var message = new Message_t();
		pos= message.unmarshall(view,pos);
		var servant = this.inst;
		var ctx = new tce.RpcContext();
		ctx.msg = m;
		servant.sendMessage(token_list,message,ctx);
		if( (m.calltype & tce.RpcMessage.ONEWAY) !=0 ){
			return true;
		}		
		
		return r;
	}	;	
	
	this.func_1_delegate = function(m){
		var r = false;
		var pos =0;
		var array = null;
		var view = null;
		array = new Uint8Array(m.paramstream);
		view = new DataView(array.buffer);
		var seqs = [];
		var _array_7 = new SIDS_thlp(seqs);
		pos=_array_7.unmarshall(view,pos);
		var servant = this.inst;
		var ctx = new tce.RpcContext();
		ctx.msg = m;
		servant.confirmMessage(seqs,ctx);
		if( (m.calltype & tce.RpcMessage.ONEWAY) !=0 ){
			return true;
		}		
		
		return r;
	}	;	
	
}

return {
	ITerminal : ITerminal,
	ITerminalProxy : ITerminalProxy	,	
	IUserEventListener : IUserEventListener,
	IUserEventListenerProxy : IUserEventListenerProxy	,	
	ITerminalGatewayServer : ITerminalGatewayServer,
	ITerminalGatewayServerProxy : ITerminalGatewayServerProxy	,	
	IMessageServer : IMessageServer,
	IMessageServerProxy : IMessageServerProxy	
};

});
