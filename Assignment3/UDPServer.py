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
from communication import *

PASS_ON_VALUE = 2

server_list = ["planetlab1.cs.ubc.ca","plonk.cs.uwaterloo.ca","planetlab03.cs.washington.edu"]

results_queue = Queue()
cache_request = {}
forwarded_request = {}
check_status_time = 30

server_address = ("", 7790)
node = Node(socket.gethostbyname(socket.gethostname()),server_address[1])
ring = Ring(node.address(), server_address[1])


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
  'update_ring': 37,
  'report_death': 38
}

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
  global node

  node_add = request['payload']

  data = None
  local_host_name = socket.getfqdn()

  if node.host != node_add:
    try:
      index = server_list.index(local_host_name)
    except:
      index = -1

    self = index

    while not data and not (node_add in ring.ring.values()):
      index = (index + 1) % len(server_list)
      if index == self:
        print "And it comes to a full circle"
        data = "self"
        break;
      successor = (server_list[index],server_address[1]);
      if socket.gethostbyname(successor[0]) != node_add:
        message = assembleMessage(34, None, node_add)
        sendRequest(message,successor,None,1)

    if request['address'][0] == node_add:
      ring.add_node(node_add)
      ring.add_node(request['address'][0])
      request['address'] = list(request['address'])
      request['address'][1] = node.port
      request['address'] = tuple(request['address'])
      ring_list = ','.join(map(str, ring.ring.values()))
      results_queue.put((request, 'update_ring', ring_list))
    else:
      results_queue.put((request, 'success', None))


    transfer_keys(node_add)

def remove_node(request):
  global ring
  global node

  delete_node = request['payload']

  if node.host != delete_node:
    ring.remove_node(delete_node)
    ring.add(request['address'][0])

    data = None
    local_host_name = socket.getfqdn()
    try:
      index = server_list.index(local_host_name)
    except:
      index = -1

    self = index

    predecessor = index - 1;

    while not server_list[predecessor] in ring.ring.values() :
      predecessor = (predecessor - 1) % len(server_list)
      if predecessor == self:
        print "And it comes to a full circle"
        break;
    if predecessor != self:
      predecessor = (socket.gethostbyname(predecessor), server_address[1])
      message = assembleMessage(38, None, delete_node)
      data = sendRequest(message,predecessor,None,1)

def forwarded(request):
  global results_queue
  global ring
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

def update_ring(request):
  ring_list = request['payload'].split(',')
  ring.update_ring(ring_list)

def transfer_keys(node_add):
  new_node = ring.hash_key(node_add)
  for k in node.data.keys():
    position = ring.get_node_position(request[k])[0]
    if position == new_node:
      message=assembleMessage(1,k,node.data[k])
      sendRequest(message,(position,server_address[1]),None,1)

command = {
  1 : node.put,
  2 : node.get,
  3 : node.remove,
  4 : shutdown,
  32 : node.put_no_overwrite,
  33 : node.report_alive,
  34 : add_node,
  35 : forwarded,
  36 : pass_on_reply,
  37 : update_ring,
  38 : remove_node
}

def node_operation (request):
  global results_queue
  if request['command'] in {1,2,3,32,33}:
    try:
      status, value = command[request['command']](request['key'], request['value'])
    except:
      status, value = "internal_failure", None

    results_queue.put((request, status, value))
  elif request['command'] in {4,34,35,36,37,38}:
    command[request['command']](request)
  else:
      no_operation(request)

def parseCommand (recv, address):
  request = {}
  request['address'] = address

  try:
    request['header'] = recv[0:16]
    request['command'] = struct.unpack_from('<b',recv, 16)
    request['command'] = request['command'][0]
    if not request['command'] in (34,35,36,37,38):
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
  global server_address
  forward = requestID(server_address[1])

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
  if request['command'] in {1,2,3,32}:
    position = ring.get_node_position(request['key'])[0]
    if position != ring.node:
      current = False
      address = (position, server_address[1])
      forward = createForward(rdata, request)
      sock.sendto(forward, address)

  if current:
    task = Thread(target=node_operation, args=(request,))
    task.start()
    task.join()

def checkSuccessor(string = None):
  global node
  global check_status_time
  data = None
  local_host_name = socket.getfqdn()
  try:
    index = server_list.index(local_host_name)
  except:
    index = -1

  self = index

  while not data:
    command = 34
    node_ip = node.host
    if string != "init":
      command = 33
      node_ip =  None

      predecessor = index - 1
      try:
        while not server_list[predecessor] in ring.ring.values() :
          predecessor = (predecessor - 1) % len(server_list)
          if predecessor == self:
            print "And it comes to a full circle"
            break;
        print predecessor, socket.gethostbyname(predecessor)
        if predecessor != self:
          predecessor = (socket.gethostbyname(predecessor), server_address[1])
          message = assembleMessage(38, None, dest_ip)
          d = sendRequest(message,predecessor,None,1)
        dest_ip = socket.gethostbyname(server_list[index])
        if dest_ip != node.host:
          predecessor = index - 1;
          print "Remove from ring: " + dest_ip
          ring.remove_node(dest_ip)

      except:
        pass
    index = (index + 1) % len(server_list)
    if index == self:
      print "And it comes to a full circle"
      data = "self"
      break;
    successor = (server_list[index],server_address[1]);
    message = assembleMessage(command, None,node_ip)
    data = sendRequest(message,successor,None,1)
    print datas
  print time.ctime()

def check_status():
  global operating
  global ring
  while operating == True:
    checkSuccessor()
    print ring.ring.values()
    time.sleep(check_status_time)



# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(server_address)
sock.setblocking(0)
operating = True

print "Listening on %s" % server_address[1]

checkSuccessor("init")

status_check = Thread(target=check_status)
status_check.daemon =True
status_check.start()

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
