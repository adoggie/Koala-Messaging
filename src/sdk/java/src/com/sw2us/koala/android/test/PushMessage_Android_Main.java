package com.sw2us.koala.android.test;

import android.app.Activity;
import android.widget.EditText;
import android.widget.Toast;
import com.sw2us.koala.client.PushMessageClient;
import com.sw2us.koala.client.PushMessageEventListener;

import java.net.InetSocketAddress;
import java.util.HashMap;

public class PushMessage_Android_Main {
	String ACCESS_ID = "0098271772";
	String SECRET_KEY = "qZmthanNk";
	String ACCOUNT = "14778920@163.com";
	String DEVICE_ID = "c2RqZmthanNkZmtsYWpzZGtmbGphc2RmCg==";
	String TAG = "cute";
	int PLATFORM = PushMessageClient.P_UNDEFINED;

	static PushMessage_Android_Main app = null;
	Activity mainview;
	EditText textview;

	public PushMessage_Android_Main(){

	}

	class TestSendThread implements Runnable{
		@Override
		public void run() {
			try {
				Thread.sleep(4 * 1000);
				PushMessageClient.instance().simpleTextAccount("test title", "meimei", ACCOUNT);
			}catch (Exception e){
				System.out.println(e.toString());
			}
		}
	}

	public void sendMessage() {
		try {
			PushMessageClient.instance().simpleTextAccount("test title", "meimei", ACCOUNT);
		}catch (Exception e){
			System.out.println(e.toString());
		}
	}

	public void init(final Activity mainview,EditText showtext){
		this.mainview = mainview;
		this.textview = showtext;

		PushMessageClient.instance().set_gws_address(new InetSocketAddress("localhost", 14001)).
				set_server_url("http://localhost:16001").set_tag(TAG);

		PushMessageClient client = PushMessageClient.instance();
		client.set_event_listener(new PushMessageEventListener() {
			@Override
			public void onSimpleText(String title, String content, HashMap<String, String> props) {
//				System.out.println("you got message:"+title +"\n" + content);
				Toast.makeText(mainview, "server got message!", Toast.LENGTH_SHORT).show();
			}
		});

		client.open(ACCESS_ID, SECRET_KEY, ACCOUNT, DEVICE_ID);

	}


	static public PushMessage_Android_Main instance(){
		if(PushMessage_Android_Main.app == null){
			app = new PushMessage_Android_Main();
		}
		return app;
	}

}
