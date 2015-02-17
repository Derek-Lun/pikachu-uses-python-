import socket
import sys
import array
import struct
import random
import time
import select

def requestID ():
  rID = bytearray()
  ip = socket.gethostbyname(socket.gethostname()).split('.')

  hostAddress = []

  for elem in ip:
    y = int(elem)
    hostAddress.append(struct.pack('<B',y))

  rID.extend(hostAddress)

  port = struct.pack('<h',localport)

  rID.extend(port)

  randomGen = struct.pack('<H', random.randint(0, 65534))

  rID.extend(randomGen)

  millis = struct.pack('<Q', long(round(time.time() * 1000)))

  rID.extend(millis)

  return rID
# We don't need this for Assignment 3
def parseID (original, received):
  match = True

  for x in range(0,16):
    o = struct.pack('<B', original[x])
    r = received[x]
    if not (o == r):
      match = False
      break

  return match

def parsePayload (received):
  if (len(received) == 1):
    payload = received
  else:
    size = struct.unpack_from('<i',received, 1)
    print size[0]
    
    r = list(received)
    for i in range(0, 20):
        r.pop(0)
    
    payload = []
    
    for i in range(size[0]):
        payload.append(r[i])

  return payload

def sendRequest (dataPayload, server_address):
  timeoutInterval = 500
  numTries = 1
  done = False

  data = requestID()

  rID = bytearray()

  for i in data:
    rID.append(i);

  data.extend(dataPayload)

  for i in data:
    print hex(i)

  while (not done) and numTries <= 3:
    try:
      # Send data
      print 'sending data'

      print 'Trying %s time' %numTries
      sent = sock.sendto(data, server_address)

      numTries += 1

      # Receive response
      print 'waiting to receive'

      sock.settimeout(timeoutInterval/1000)
      data, server = sock.recvfrom(16384)

      if data:
        print "done: ", data
        done = True
        return data
    except socket.error:
      if numTries > 3:
        print 'Exceed maximum of tries, server may be down.'
        break;
      timeoutInterval *= 2
      print 'Timeout. Doubling timeout to %s ms.' % timeoutInterval

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

localport = 4000

server_address = ('localhost', 7778)

message = struct.pack('<I', 05)

data = sendRequest(message, server_address)

if data:
  print parsePayload(data)
