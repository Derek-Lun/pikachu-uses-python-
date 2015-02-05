package com.eece411.A2;

import com.eece411.*;

public class MonitoringService {

	public static void main(String[] args)
	{
		Thread replyThread = new Thread(new ReplyService());
		Thread RequestThread = new Thread(new RequestService());
		
		replyThread.start();
		RequestThread.start();
	}
}
