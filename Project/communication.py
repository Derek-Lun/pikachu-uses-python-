import struct
import random
import array
import time
import select
import socket
import datetime

localport = 4000
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def requestID (port):
  rID = bytearray()
  ip = socket.gethostbyname(socket.gethostname()).split('.')

  hostAddress = []

  for elem in ip:
    y = int(elem)
    hostAddress.append(struct.pack('<B',y))

  rID.extend(hostAddress)

  port = struct.pack('<h',port)

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
  print res_code
  r = ''.join(r)

  size = struct.unpack_from('<h', r)[0]

  payload = []
  for i in range(size):
    payload.append(r[i+2])

  return res_code,payload

def sendRequest (dataPayload, server_address,file_object = None, max_tries=3):
  timeoutInterval = 1000
  numTries = 1
  done = False

  data = requestID(server_address[1])

  rID = bytearray()

  for i in data:
    rID.append(i);
    
  data.extend(dataPayload)

  while (not done) and numTries <= max_tries:
    try:
      # Send data
      print 'sending data to ' + server_address[0] 
      print 'Trying %s time' %numTries
      if file_object:
      # Start timer for Turnaround time
        timer = startTimer() 
      
      sent = sock.sendto(data, server_address)

      numTries += 1

      # Receive response
      #print 'waiting to receive'

      sock.settimeout(timeoutInterval/1000)
      data, server = sock.recvfrom(16384)

      #if parseID(rID, data):
      if len(data) >= 16:
        done = True
        if file_object:
          # End timer and print Turnaround time
          endTimer(timer,file_object)
        return data, server
    except socket.error as serr:
      print serr
      if numTries > max_tries:
        print 'Exceed maximum of tries, server may be down.'
        break
      timeoutInterval *= 2
      print 'Timeout. Doubling timeout to %s ms.' % timeoutInterval
  return None, None

def assembleMessage(commandNum,keyString=None,valueString=None):
    #Define each byte array with fixed size
    messageBuff = bytearray()
    commandBuff = bytearray(1)
    keyBuff = bytearray(32)
    vLengthBuff = bytearray(2)
    valueBuff = bytearray(15000)


    #Put value in byte array

    commandBuff = struct.pack ('<b',commandNum)
    messageBuff.extend(commandBuff)
    
    if not commandNum in (4,33,34,38):
        index = 0
        for letter in keyString:    
            struct.pack_into('<s',keyBuff,index,letter)
            index += 1
        messageBuff.extend(keyBuff)


    if valueString:
        vLengthBuff = struct.pack ('<h',len(valueString))
        valueBuff=valueString
        messageBuff.extend(vLengthBuff)
        messageBuff.extend(valueBuff)
    else:
        if commandNum in (1,32):
            messageBuff.extend(struct.pack ('<h',0))

    return messageBuff    
    
    

def startTimer():
  #start timer
  return datetime.datetime.now()
    
def endTimer(timer):
  #end timer and calculate turnAroundTime
  turnAroundTime = (datetime.datetime.now()-timer)
  
  time = str(round((float(int(turnAroundTime.seconds)*1000000 + turnAroundTime.microseconds) /1000.0),2))
  
  return time
  

def printTurnAroundTime (time):
  print "\nTurnaround Time: "+time+" ms\n"
  
def writeTurnAroundTime (time,file_object):  
  file_object.write("Turnaround Time: "+time+" ms\n\n")