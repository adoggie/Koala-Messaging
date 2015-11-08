package com.sw2us.koala.client;

import java.util.HashMap;

/**
 * Created by scott on 11/7/15.
 */
public interface PushMessageEventListener {
	void onSimpleText(String title,String content,HashMap<String,String> props);
}
