package com.example.myapp;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import com.sw2us.koala.android.test.PushMessage_Android_Main;


public class MyActivity extends Activity {
	/**
	 * Called when the activity is first created.
	 */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main);
		Button btn = (Button)this.findViewById(R.id.button1);
		btn.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View arg0) {
				PushMessage_Android_Main.instance().sendMessage();
			}

		});

		EditText text = (EditText) findViewById(R.id.editText);
		PushMessage_Android_Main.instance().init(this,text);
	}
}
