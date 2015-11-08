package com.sw2us.koala.client;

import java.net.InetSocketAddress;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Vector;

//import net.sf.json.*;
import org.apache.http.* ;
//import net.sf.json.* ;

import org.apache.http.protocol.HTTP;
import org.json.simple.JSONObject;

//import java.net.URL;
import com.sw2us.koala.*;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.json.simple.JSONValue;
import tce.RpcCommunicator;

/**
 * Created by scott on 11/7/15.
 */
public class PushMessageClient implements Runnable{

	public final static  int P_UNDEFINED = 0;
	public final static  int P_ANDROID = 1;
	public final static  int P_IOS = 2;
	public final static  int P_DESKTOP = 4;
	public final static  int P_HTML5 = 8;
	public final static  int P_ALL = P_ANDROID | P_IOS | P_DESKTOP | P_HTML5;

	ITerminalGatewayServerProxy _prx_gws = null;
	IMessageServerProxy _prx_mexs = null;
	int     _ping = 5;
	InetSocketAddress _gws_address = InetSocketAddress.createUnresolved("localhost",14001);

	String _access_id;
	String _secret_key;
	String _account;
	String _device_id;



	String _tag = "";
	int   _platform = P_DESKTOP;
	String _token = null;

	boolean _is_running = false;
	Thread _bg_thread = null;
	Object _ev_wait = new Object();

	PushMessageEventListener _event_listener = null;


	public PushMessageEventListener get_event_listener() {
		return _event_listener;
	}

	public PushMessageClient set_event_listener(PushMessageEventListener _event_listener) {
		this._event_listener = _event_listener;
		return this;
	}

	public boolean is_ssl_enable() {
		return _ssl_enable;
	}

	public PushMessageClient set_ssl_enable(boolean _ssl_enable) {
		this._ssl_enable = _ssl_enable;
		return this;
	}


	public String get_tag() {
		return _tag;
	}

	public PushMessageClient set_tag(String _tag) {
		this._tag = _tag;
		return this;
	}

	public InetSocketAddress get_gws_address() {
		return _gws_address;
	}

	public PushMessageClient set_gws_address(InetSocketAddress _gws_address) {
		this._gws_address = _gws_address;
		return this;
	}

	public int get_ping() {
		return _ping;
	}

	public PushMessageClient set_ping(int _ping) {
		this._ping = _ping;
		return this;
	}

	boolean _ssl_enable = false;

	public String get_server_url() {
		return _server_url;
	}

	public PushMessageClient set_server_url(String _server_url) {
		this._server_url = _server_url;
		return this;
	}

	String _server_url = "";

	public  PushMessageClient(){
		init_rpc();
	}

	static PushMessageClient handle = null;
	public  static PushMessageClient instance(){
		if( PushMessageClient.handle == null){
			PushMessageClient.handle = new PushMessageClient();
		}
		return PushMessageClient.handle;
	}

	protected boolean init_rpc(){
		tce.RpcCommunicator.instance().init("pushmessage_client", null);
		return true ;
	}

	public boolean open(String access_id, String secret_key, String account, String device_id) {
		_access_id = access_id;
		_secret_key = secret_key;
		_account = account;
		_device_id = device_id;

		_prx_gws = ITerminalGatewayServerProxy.create(_gws_address.getHostString(),_gws_address.getPort(),_ssl_enable);
		_prx_mexs = IMessageServerProxy.createWithProxy(_prx_gws);

		tce.RpcCommAdapter adapter =  tce.RpcCommunicator.instance().createAdapterWithProxy("terminal_adapter", _prx_gws);
		TerminalImpl servant = new TerminalImpl(this);
		adapter.addServant(servant);

		_bg_thread = new Thread(this);
		_bg_thread.start();
		return true;
	}

	public void close(){
		_is_running = false;
		_token = null;
		_ev_wait.notify();
	}

	boolean register(){
		String url = _server_url;

		url = url + "/api/push/register/";
		HttpPost post = new HttpPost( url );
		List< NameValuePair> params = new ArrayList< NameValuePair>();
		params.add( new BasicNameValuePair("access_id",_access_id));
		params.add( new BasicNameValuePair("secret_key",_secret_key));
		params.add( new BasicNameValuePair("account",_account));
		params.add( new BasicNameValuePair("device_id",_device_id));
		params.add( new BasicNameValuePair("tag",_tag));
		params.add(new BasicNameValuePair("platform", String.valueOf(_platform)));
		try {
//			post.setEntity(new UrlEncodedFormEntity(params, Charset.forName("Utf-8")));
			post.setEntity(new UrlEncodedFormEntity(params, HTTP.UTF_8));
			HttpResponse response = new DefaultHttpClient().execute(post);
			if (response.getStatusLine().getStatusCode() != 200){
				return false;
			}
			String result = EntityUtils.toString(response.getEntity());

			Object object = JSONValue.parse(result);
			HashMap<String,Object> values = (HashMap<String,Object>)(object);
			JSONObject jsonobj = (JSONObject)object;
			if ( Integer.valueOf(jsonobj.get("status").toString() ) == 0){
				Object token = jsonobj.get("result");
				_token = token.toString();
				_prx_gws.setToken(_token);
			}
//			System.out.println(jsonobj.toString());

		}catch (Exception e){
//			e.printStackTrace();
			System.out.println("register() failed: "+ e.toString());
			return false;
		}

		return true;
	}

	public boolean simpleTextAccount(String title,String content,String account){
		return simpleTextAccount( title,content,account,_access_id,_secret_key,P_UNDEFINED);
	}

	public boolean simpleTextAccount(String title,String content,String account,String access_id,String secret_key,int Platform){
		String url = _server_url;

		url = url + "/api/push/simple/account/";
		HttpPost post = new HttpPost( url );
		List< NameValuePair> params = new ArrayList< NameValuePair>();
		params.add( new BasicNameValuePair("access_id",access_id));
		params.add( new BasicNameValuePair("secret_key",secret_key));
		params.add( new BasicNameValuePair("account",account));
		params.add( new BasicNameValuePair("title",title));
		params.add( new BasicNameValuePair("content",content));
		params.add(new BasicNameValuePair("platform", String.valueOf(_platform)));
		try {
//			post.setEntity(new UrlEncodedFormEntity(params, Charset.forName("Utf-8")));
			post.setEntity(new UrlEncodedFormEntity(params,HTTP.UTF_8));
			HttpResponse response = new DefaultHttpClient().execute(post);
			if (response.getStatusLine().getStatusCode() != 200){
				return false;
			}
			String result = EntityUtils.toString(response.getEntity());

			Object object = JSONValue.parse(result);
			HashMap<String,Object> values = (HashMap<String,Object>)(object);
			JSONObject jsonobj = (JSONObject)object;
			if ( Integer.valueOf(jsonobj.get("status").toString() ) != 0){
				System.out.println(jsonobj.get("errcode"));
				return false;
			}
		}catch (Exception e){
			e.printStackTrace();
			return false;
		}

		return true;
	}

	@Override
	public void run() {
		_is_running = true;
//		_ev_wait = new Object();
		while(_is_running){
			try {
				if( _token == null){
					System.out.println("ready to register..");
					register();
				}
				if( _token != null){
					keep_alive();
				}
				synchronized (_ev_wait) {
					_ev_wait.wait(_ping * 1000);
				}
			}catch (Exception e){
				e.printStackTrace();
			}

		}
		System.out.println("background thread exiting..");
	}

	void keep_alive(){
		try{
			System.out.println("do keep_alive..");
			_prx_gws.ping_oneway(null);
		}catch (Exception e){
			e.printStackTrace();
		}
	}

	public void waitForShutdown(){
		tce.RpcCommunicator.instance().waitForShutdown();
	}


	void onSimpleText(SimpleText_t text){ // String title,String content,HashMap<String,String> props){
		HashMap<String,String>  props = new HashMap<String,String>();
		if( _event_listener!=null){
			_event_listener.onSimpleText( text.title,text.content,props);
		}
		this.confirmMessage(text.seq);
	}

	void confirmMessage(String sequence){
		try{
			Vector<String> ids = new Vector<String>();
			ids.add(sequence);
			_prx_mexs.confirmMessage_oneway( ids,null);
		}catch (Exception e){
			System.out.println(e.toString());
		}
	}
}
