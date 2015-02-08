package com.eece411.A2;

public class RequestService implements Runnable {

	public void run() {
		System.out.println("request service!");
		
		while (MonitoringService.isRunning) {

		}
	}
}
