import socket
import struct
from threading import Timer
import binascii
from Queue import Queue
from threading import Thread

results_queue = Queue()
data = {}
cache_request = {}

def put (request):
  print 'Operation: put'
  global results_queue
  d = {request['key']: request['value']}
  data.update(d)
  results_queue.put((request, 'success', None))

def put_no_overwrite (request):
  print 'Operation: put without overwrite'
  global results_queue
  if request['key'] not in data:
    put(request)
  results_queue.put((request, 'key_exist', None))

def get (request):
  print 'Operation: get'
  global results_queue
  if request['key'] in data:
    results_queue.put((request,'success', data.get(request['key'])))
  results_queue.put((request, 'dne', None))

def remove (request):
  print 'Operation: remove'
  global results_queue
  if request['key'] in data:
    data.pop(request['key'], None)
    results_queue.put((request, 'success', None))
  results_queue.put((request, 'dne', None))

def shutdown (request):
  print 'Operation: shutdown'
  global results_queue
  global operating
  operating = False
  print "Shutting down..."
  results_queue.put((request, 'success', None))

def no_operation(request):
  print 'Operation: do not recognize'
  global results_queue
  results_queue.put((request, 'do_not_recognize', None))

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

def parseCommand (recv, address):
  request = {}
  request['address'] = address

  try:
    request['header'] = recv[0:16]
    request['command'] = struct.unpack_from('<b',recv, 16)
    request['command'] = request['command'][0]
    request['key'] = recv[17:49].split(b'\0',1)[0]

    if request['command'] == 1 or request['command'] == 32:
      length = struct.unpack_from('<h', recv, 49)
      begin = 51
      request['value'] = recv[begin:begin+length[0]]

  except:
    request['command'] = no_operation

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

server_address = ("0.0.0.0", 7790)

sock.bind(server_address) 

operating = True

print "Listening on %s" % server_address[1]

while operating == True:
  
  if not results_queue.empty():
    result = results_queue.get()
    reply = createReply(result[0], result[1], result[2])
    sock.sendto(reply, result[0]['address'])
    cacheMsg(rdata[0:16],reply)

  try:
    rdata, address = sock.recvfrom(16384)
    func = None
    try:
      cache = cacheMsg(rdata[0:16])
      if cache:
        sock.sendto(cache, address)
        continue

      req = parseCommand(rdata, address)
      print "Received: ", 
      print req

      func = command[req['command']]
    except:
      func = no_operation

    task = Thread(target=func, args=((req),))
    task.start()
    task.join()

  except socket.error: 
      #print "Socket closed"
      pass
