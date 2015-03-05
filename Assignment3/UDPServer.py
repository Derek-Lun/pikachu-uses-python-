import socket
import struct
from threading import Timer
import binascii
from Queue import Queue
from threading import Thread
from node import *
from ring import *

results_queue = Queue()
data = {}
cache_request = {}

server_address = ("0.0.0.0", 7790)
node = Node(socket.gethostbyname(socket.gethostname()),server_address[1])
ring = Ring(node.address())

def shutdown (request):
  print 'Operation: shutdown'
  global results_queue
  global operating
  operating = False
  print "Shutting down..."
  return 'success', None

def no_operation(request):
  print 'Operation: do not recognize'
  global results_queue
  results_queue.put((request, 'do_not_recognize', None))

def add_node(request):
  global ring
  node = request['address'][0] + ":" + str(request['address'][1])
  ring.add_node(node)
  results_queue.put((request, 'success', None))

command = {
  1 : node.put,
  2 : node.get,
  3 : node.remove,
  4 : shutdown,
  32 : node.put_no_overwrite,
  33 : node.report_alive,
  34 : add_node
}

def node_operation (request):
  global results_queue
  global node
  
  if request['command'] in (1,2,3,32,33):
    try:
      status, value = command[request['command']](request['key'], request['value'])
      print status
    except:
      status, value = "internal_failure", None

    results_queue.put((request, status, value))
  elif request['command'] in (4,34): 
    command[request['command']](request)
  else:
      no_operation(request)

response_status = {
  'success': 0,
  'dne': 1,
  'oos': 2,
  'sys_overload': 3,
  'internal_failure': 4,
  'do_not_recognize': 5,
  'key_exist' : 32,
  'alive': 34
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
    else:
      request['value'] = None

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
    #print "Removing cache with id: " + binascii.hexlify(id)
    cache_request.pop(id, None)
  
def routeMessage(rdata, request):
  current = True
  if request['command'] in (1,2,3,32):
    position = ring.get_node_position(request['key'])[0]
    if position != ring.node:
      current = False
      print position.split(':')


  if current:
    task = Thread(target=node_operation, args=((request),))
    task.start()
    task.join()

  
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(server_address) 

operating = True

print "Listening on %s" % server_address[1]

while operating == True:
  
  if not r esults_queue.empty():
    result = results_queue.get()
    reply = createReply(result[0], result[1], result[2])
    sock.sendto(reply, result[0]['address'])
    cacheMsg(rdata[0:16],reply)

  try:
    rdata, address = sock.recvfrom(16384)
    func = None

    cache = cacheMsg(rdata[0:16])
    if cache:
        sock.sendto(cache, address)
        continue

    req = parseCommand(rdata, address)
    print "Received: ", 
    print req

    routeMessage(rdata, req)

  except socket.error: 
      #print "Socket closed"
      pass
