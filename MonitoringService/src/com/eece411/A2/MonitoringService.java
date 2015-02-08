package com.eece411.A2;

import com.eece411.*;

public class MonitoringService {

	static boolean isRunning = true;
	
	public static void main(String[] args)
	{
		Thread replyThread = new Thread(new ReplyService());
		Thread requestThread = new Thread(new RequestService());
		
		replyThread.start();
		requestThread.start();
	}
}
