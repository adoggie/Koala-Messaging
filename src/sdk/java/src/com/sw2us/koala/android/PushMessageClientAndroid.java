package com.sw2us.koala.android;

import com.sw2us.koala.client.PushMessageClient;
import tce.android.RpcCommunicator_Android;

/**
 * Created by scott on 11/8/15.
 */
public class PushMessageClientAndroid extends PushMessageClient {
	@Override
	protected boolean init_rpc() {
		RpcCommunicator_Android.instance().init("test",null);
		return true;
	}
}
