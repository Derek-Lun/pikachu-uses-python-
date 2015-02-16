import socket
import sys
import array
import struct
import random
import time

def requestID ():
  rID = bytearray()
  ip = socket.gethostbyname(socket.gethostname()).split('.')

  hostAddress = []

  for elem in ip:
    y = int(elem)
    hostAddress.append(struct.pack('!B',y))

  hostAddress.reverse()

  rID.extend(hostAddress)

  port = struct.pack('<h',localport)

  rID.extend(port)

  randomGen = struct.pack('<H', random.randint(0, 65534))

  rID.extend(randomGen)

  millis = struct.pack('<Q', long(round(time.time() * 1000)))

  rID.extend(millis)

  return rID


def sendRequest (dataPayload, hostname, port):
  timeoutInterval = 100
  numTries = 1
  done = False
  # while (not done)&& numTries <= 3:
  #   try:
  #     # Send data
  #     print 'sending "%s"' % message
  #     #generate request ID
  #     sent = sock.sendto(message, server_address)
  #     sent.settimeout(timeoutInterval/1000)

  #     # Receive response
  #     print 'waiting to receive'
  #     data, server = sock.recvfrom(localport)
  #     # check if requestID is the same
  #     done = True
  #     numTries++
  #     print 'received "%s"' % data
  #   except socket.timeout:
  #     timeoutInterval *= 2
  #     print 'Timeout. Doubling timeout to "%s" ms.' % timeoutInterval

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = 'This is the message.  It will be repeated.'

localport = 4000

requestID()
