import struct
import random
import array
import time
import select
import socket

localport = 4000
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
  r = list(received)
  for i in range(0, 16):
    r.pop(0)
  res_code = ord(r[0])
  r.pop(0)
  
  r = ''.join(r)

  size = struct.unpack_from('<i', r)[0]

  payload = []

  for i in range(size):
    payload.append(r[i+4])

  return res_code,payload

def sendRequest (dataPayload, server_address):
  timeoutInterval = 1000
  numTries = 1
  done = False

  data = requestID()

  rID = bytearray()

  for i in data:
    rID.append(i);
    
  data.extend(dataPayload)

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

      #if parseID(rID, data):
      if len(data) >= 16:
        done = True

        return data
    except socket.error:
      if numTries > 3:
        print 'Exceed maximum of tries, server may be down.'
        break
      timeoutInterval *= 2
      print 'Timeout. Doubling timeout to %s ms.' % timeoutInterval

def assembleMessage(commandNum,keyString=None,valueString=None):
    #Define each byte array with fixed size
    messageBuff = bytearray()
    commandBuff = bytearray(1)
    keyBuff = bytearray(32)
    vLengthBuff = bytearray(2)
    valueBuff = bytearray(15000)


    #Put value in byte array

    commandBuff = struct.pack ('<b',commandNum)

    index = 0
    for letter in keyString:    
        struct.pack_into('<s',keyBuff,index,letter)
        index += 1

    messageBuff.extend(commandBuff)
    messageBuff.extend(keyBuff)

    if valueString:
        valueBuff=valueString
        vLengthBuff = struct.pack ('<h',len(valueString))
        messageBuff.extend(vLengthBuff)
        messageBuff.extend(valueBuff)
    
    return messageBuff    