package com.eece411.A2;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;

import com.matei.eece411.util.ByteOrder;

public class ReplyService implements Runnable {
	static final int udpHeaderSize = 16;
	
	public void run(){
		System.out.println("reply service!");
		
        byte[] receiveData = new byte[1024];
        byte[] sendData = new byte[1024];			
        try {
			DatagramSocket serverSocket = new DatagramSocket(3808);
			
			while (MonitoringService.isRunning) {
				
				DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
                serverSocket.receive(receivePacket);
                
        		InetAddress srcIp = receivePacket.getAddress();
                int srcPort = receivePacket.getPort();
                
                createReplyHead(sendData, receiveData);
                receiveData[16] = 0x00;
                receiveData[17] = 0x55; //suppose to be some info
                
                DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, srcIp, srcPort);
                serverSocket.send(sendPacket);
                
			}
			serverSocket.close();
		} catch (SocketException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			MonitoringService.isRunning = false;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			MonitoringService.isRunning = false;
		}
	}
	
	static private void createReplyHead(byte[] sendData, byte[] recieveData)
	{
		for(int i = 0; i < udpHeaderSize; i++)
			sendData[i] = recieveData[i];
	}
}
