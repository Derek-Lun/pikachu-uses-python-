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


def sendRequest (dataPayload, server_address):
  timeoutInterval = 100
  numTries = 1
  done = False

  data = requestID()

  data.extend(dataPayload)

  for i in data:
    print hex(i)

  while (not done) and numTries <= 3:
    try:
      # Send data
      print 'sending data'

      # sock.setblocking(1)
      sock.settimeout(timeoutInterval/1000)
      sent = sock.sendto(data, server_address)

      numTries += 1

      # Receive response
      print 'waiting to receive'
      data, server = sock.recvfrom(server_address[1])
      # check if requestID is the same
      done = True
      print 'received "%s"' % data
    except socket.error:
      timeoutInterval *= 2
      print 'Timeout. Doubling timeout to "%s" ms.' % timeoutInterval

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 5627)
message = struct.pack('<I', 909090)

localport = 4000

sendRequest(message, server_address)


