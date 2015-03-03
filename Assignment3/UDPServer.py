import socket
import struct
from threading import Timer
import binascii


data = {}
cache_request = {}

def put (request):
  print 'Operation: put'
  d = {request['key']: request['value']}
  data.update(d)
  return 'success', None

def put_no_overwrite (request):
  print 'Operation: put without overwrite'
  if request['key'] not in data:
    return put(request)
  return 'key_exist', None

def get (request):
  print 'Operation: get'
  if request['key'] in data:
    return 'success', data.get(request['key'])
  return 'dne', None 

def remove (request):
  print 'Operation: remove'
  if request['key'] in data:
    data.pop(request['key'], None)
    return 'success', None
  return 'dne', None 

def shutdown (request):
  print 'Operation: shutdown'
  global operating
  operating = False
  print "Shutting down..."
  return 'success', None

command = {
  1 : put,
  2 : get,
  3 : remove,
  4 : shutdown,
  32 : put_no_overwrite
}

response_status = {
  'success': 0,
  'dne': 1,
  'oos': 2,
  'sys_overload': 3,
  'internal_failure': 4,
  'do_not_recognize': 5,
  'key_exist' : 32
}

def parseCommand (recv):
  request = {}

  try:
    request['header'] = recv[0:15]
    request['command'] = struct.unpack_from('<b',recv, 16)
    request['command'] = request['command'][0]
    request['key'] = recv[17:49].split(b'\0',1)[0]

    if request['command'] == 1 or request['command'] == 32:
      length = struct.unpack_from('<h', recv, 49)
      begin = 51
      request['value'] = recv[begin:begin+length[0]]

  except:
    request['command'] = None

  return request

def createReply (request,status, value = None):
  reply = bytearray()
  for i in request['header']:
    reply.append(i)
  reply.append(struct.pack('<b',response_status[status]))

  if value:
    length = len(value)
    reply.extend(struct.pack('<i', length))
    reply.extend(value)
  else:
    reply.extend(struct.pack('<i', 0))
    
  reply_str = "";  
  for i in reply:
    reply_str = reply_str + struct.pack('<B',i)

  return reply_str

def cacheMsg(id,reply = None):
  if reply:
    if not id in cache_request:
        cache_request.update({id: reply})
        t = Timer(5.0, removeCache,[id])
        t.start()
  else:
    return cache_request.get(id)

def removeCache(id):
  if id in cache_request:
    print "Removing cache with id: " + binascii.hexlify(id)
    cache_request.pop(id, None)
  
  
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 7790)

sock.bind(server_address)

operating = True

print "Listening on %s" % server_address[1]

while True and operating == True:
  try:
      rdata, address = sock.recvfrom(16384)
      if len(rdata) > 16:
        cache = cacheMsg(rdata[0:15])
        if not cache:
            req = parseCommand(rdata)
            print "Received: ", 
            print req
            if req['command'] in command:
              
                func = command[req['command']]
                status,value = func(req) 
                
                reply = createReply(req,status,value)
                sock.sendto(reply, address)
                cacheMsg(rdata[0:15],reply)
                print list(data)
            else:
                print 'invalid command'
                reply = createReply(req,'do_not_recognize',None)
                sock.sendto(reply, address) 
        else:
            sock.sendto(cache, address)    
  except socket.error: 
      #print "Socket closed"
      pass
