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
import sys
import datetime

PASS_ON_VALUE = 2
NUM_TRIES = 1

time_to_update = 60 * 10

central_node_hostname = 'ec2-54-69-57-23.us-west-2.compute.amazonaws.com'
central_node_port = 8888

server_list = [line.strip() for line in open('node.txt')]

results_queue = Queue()
cache_request = {}
forwarded_req_address = {}
check_status_time = 43

value_op = {1,2,3,32}
membership_op = {4,33,34,35,36,37,38}

server_port = 7790
ring = Ring(Node(socket.gethostbyname(socket.gethostname()),server_port), server_port)

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
  if not request['address'][0] in ring.ring.values():
    results_queue.put((request, 'do_not_recognize', None))

def add_node(request):
  global ring

  node_add = request['payload']
  
  if (ring.node.host != node_add) and not (node_add in ring.ring.values()):
    ring.add_node(node_add)

    transfer_keys(node_add)

def remove_node(request):
  global ring

  delete_node = request['payload']
  if ring.node.host != delete_node and (delete_node in ring.ring.values()):
    ring.remove_node(delete_node)  

def forwarded_request(request):
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

  if str(request['header']) in forwarded_req_address:
    results_queue.put((payload, forwarded_req_address[str(request['header'])]))
    del forwarded_req_address[str(request['header'])]

def update_ring(request):
  ring_list = request['payload'].split(',')
  ring.update_ring(ring_list)

def transfer_keys(node_add):
  for k in ring.node.data.keys():
    position = ring.get_node_with_replica(k)
    if node_add in position:
      message=assembleMessage(1,k,ring.node.data[k])
      sendRequest(message,(node_add,server_port),None,1)
    if not ring.node.host in position:
      ring.node.remove(k)

def report_alive(request):
  print ring.ring.values()
  send_alive(request['address'][1])

command = {
  1 : ring.node.put,
  2 : ring.node.get,
  3 : ring.node.remove,
  4 : shutdown,
  32 : ring.node.put_no_overwrite,
  33 : report_alive,
  34 : add_node,
  35 : forwarded_request,
  36 : pass_on_reply,
  37 : update_ring,
  38 : remove_node
}

def operation (request):
  global results_queue
  if request['command'] in value_op:
    try:
      status, value = command[request['command']](request['key'], request['value'])
    except:
      status, value = "internal_failure", None

    results_queue.put((request, status, value))
  elif request['command'] in membership_op:
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

  reply_str = ""
  for i in reply:
    reply_str = reply_str + struct.pack('<B',i)

  return reply_str


def cacheMsg(id,reply = None):
  if reply:
    if not id in cache_request:
        cache_request.update({id: (reply, time.time())})
        print "Cached request"
  else:
    data = cache_request.get(id)
    if data:
      print "Using Cached response: " + data[0]
      return data[0]

def removeCache():
  while operating == True:
   try:
    for id, data in cache_request.iteritems():
      if time.time() > data[1] + 5:
	print "Removing cache: " + id 
        cache_request.pop(id, None)
    time.sleep(1)
   except RuntimeError:
	print "Removed cache"

def package_forward (raw_data, request, target_nodes, local):
  global forwarded_req_address
  forward = requestID(server_port)

  if not local:
    forwarded_req_address[str(forward)] = request['address']

  forward.append(struct.pack('<b',response_status['forwarded']))
  forward.extend(struct.pack('<h', len(rdata)))
  forward.extend(rdata)

  forward_str = ""
  for x in forward:
    forward_str = forward_str + struct.pack('<B', x)

  for t in target_nodes:
    address = (t, server_port)
    sock.sendto(forward_str, address)


def routeMessage(raw_data, request):
  local = False
  if request['command'] in value_op:
    target_nodes = ring.get_node_with_replica(request['key'])

    print target_nodes

    if ring.node.host in target_nodes:
      target_nodes.remove(ring.node.host)
      local = True
      if (request['command'] == 2) and not ring.node.key_exist(request['key']):
        local = False

    package_forward(raw_data, request, target_nodes, local)

  if (request['command'] not in value_op) or local or (len(ring.ring.values()) == 1):
    task = Thread(target=operation, args=(request,))
    task.start()
    task.join()

def send_alive(port):
  message = assembleMessage(34, None, ring.node.host)
  data = addRequestID(message, server_port)
  sock.sendto(data, (central_node_hostname, port))

def reply_response():
  global results_queue
  while operating == True:
    if not results_queue.empty():
      print "queue size"
      print results_queue.qsize()
      result = results_queue.get()
      if len(result) > 2:
        reply = createReply(result[0], result[1], result[2])
        sock.sendto(reply, result[0]['address'])
        cacheMsg(rdata[0:16],reply)
      else:
        sock.sendto(result[0], result[1])
        cacheMsg(result[0][0:16], result[0])

def resync_nodes():
  send_alive(central_node_port)
  time.sleep(time_to_update)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("", 7790)
sock.bind(server_address)
operating = True

print "Listening on %s" % server_port

check_status = Thread(target=resync_nodes)
check_status.daemon =True
check_status.start()

reply_thread = Thread(target=reply_response)
reply_thread.daemon =True
reply_thread.start()

reply_thread = Thread(target=removeCache)
reply_thread.daemon =True
reply_thread.start()

while operating == True:
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

sys.exit()
