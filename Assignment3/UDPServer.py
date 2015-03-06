import socket
import struct
import random
import time
from threading import Timer
import binascii
from Queue import Queue
from threading import Thread
from node import *
from ring import *

results_queue = Queue()
cache_request = {}
forwarded_request = {}

server_address = ("", 7790)
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

def forwarded(request):
  global results_queue
  global ring
  node = request['address'][0] + ":" + str(request['address'][1])
  ring.add_node(node)
  payload = request['payload']
  req = parseCommand(payload, request['address'])

  try:
    status, value = command[req['command']](req['key'], req['value'])
  except:
    status, value = "internal_failure", None

  payload = createReply(req, status, value)
  results_queue.put((request, 'f_reply', payload))

def pass_on_reply(request):
  global results_queue

  payload = request['payload']
  results_queue.put((payload, forwarded_request[str(request['header'])]))
  
command = {
  1 : node.put,
  2 : node.get,
  3 : node.remove,
  4 : shutdown,
  32 : node.put_no_overwrite,
  33 : node.report_alive,
  34 : add_node,
  35 : forwarded,
  36 : pass_on_reply
}

def node_operation (request):
  global results_queue

  if request['command'] in (1,2,3,32,33):
    try:
      status, value = command[request['command']](request['key'], request['value'])
    except:
      status, value = "internal_failure", None

    results_queue.put((request, status, value))
  elif request['command'] in (4,34,35,36):
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
  'alive': 34,
  'forwarded': 35,
  'f_reply': 36,
}

def requestID ():
  global server_address
  rID = bytearray()
  ip = socket.gethostbyname(socket.gethostname()).split('.')

  hostAddress = []

  for elem in ip:
    y = int(elem)
    hostAddress.append(struct.pack('<B',y))

  rID.extend(hostAddress)

  port = struct.pack('<h',server_address[1])

  rID.extend(port)

  randomGen = struct.pack('<H', random.randint(0, 65534))

  rID.extend(randomGen)

  millis = struct.pack('<Q', long(round(time.time() * 1000)))

  rID.extend(millis)

  return rID


def parseCommand (recv, address):
  request = {}
  request['address'] = address

  try:
    request['header'] = recv[0:16]
    request['command'] = struct.unpack_from('<b',recv, 16)
    request['command'] = request['command'][0]
    if not request['command'] in (35,36):
      request['key'] = recv[17:49].split(b'\0',1)[0]

      if request['command'] == 1 or request['command'] == 32:
        length = struct.unpack_from('<h', recv, 49)
        begin = 51
        request['value'] = recv[begin:begin+length[0]]
      else:
        request['value'] = None
    else:
      length = struct.unpack_from('<h', recv, 16)
      begin = 19
      request['payload'] = recv[begin:begin+length[0]]

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
    reply.extend(struct.pack('<h', length))
    reply.extend(value)
  else:
    reply.extend(struct.pack('<h', 0))

  reply_str = "";
  for i in reply:
    reply_str = reply_str + struct.pack('<B',i)

  return reply_str

def createForward (rdata, request):
  global forwarded_request
  forward = requestID()

  forwarded_request[str(forward)] = request['address']

  forward.append(struct.pack('<b',response_status['forwarded']))
  forward.extend(struct.pack('<h', len(rdata)))
  forward.extend(rdata)

  forward_str = "";
  for x in forward:
    forward_str = forward_str + struct.pack('<B', x)

  return forward_str


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
      position = position.split(':')
      address = (position[0], int(position[1]))
      forward = createForward(rdata, request)
      sock.sendto(forward, address)

  if current:
    task = Thread(target=node_operation, args=((request),))
    task.start()
    task.join()


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(server_address)

operating = True

print "Listening on %s" % server_address[1]

ring.intialization()

while operating == True:

  if not results_queue.empty():
    result = results_queue.get()
    if len(result) > 2:
      reply = createReply(result[0], result[1], result[2])
      sock.sendto(reply, result[0]['address'])
      cacheMsg(rdata[0:16],reply)
    else:
      sock.sendto(result[0], result[1])
      cacheMsg(result[0][0:16], result[0])


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
