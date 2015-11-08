package com.sw2us.koala.client.test;

import com.sw2us.koala.client.PushMessageClient;
import com.sw2us.koala.client.PushMessageEventListener;

import java.net.InetSocketAddress;
import java.util.HashMap;

public class PushMessage_Client_Main {
	String ACCESS_ID = "0098271772";
	String SECRET_KEY = "qZmthanNk";
	String ACCOUNT = "14778920@163.com";
	String DEVICE_ID = "c2RqZmthanNkZmtsYWpzZGtmbGphc2RmCg==";
	String TAG = "cute";
	int PLATFORM = PushMessageClient.P_UNDEFINED;

	static PushMessage_Client_Main app = null;

	public PushMessage_Client_Main(){

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

	void run(){
		PushMessageClient.instance().set_gws_address(new InetSocketAddress("localhost", 14001)).
				set_server_url("http://localhost:16001").set_tag(TAG);
		PushMessageClient client = PushMessageClient.instance();
		client.set_event_listener(new PushMessageEventListener() {
			@Override
			public void onSimpleText(String title, String content, HashMap<String, String> props) {
				System.out.println("you got message:"+title +"\n" + content);
			}
		});

		client.open(ACCESS_ID, SECRET_KEY, ACCOUNT, DEVICE_ID);

		Thread thread = new Thread( new TestSendThread());
		thread.start();
		System.out.println("waiting for shutdown..");
		PushMessageClient.instance().waitForShutdown();
	}

	public static void main(String[] args) {
		new PushMessage_Client_Main().run();


	}

}
