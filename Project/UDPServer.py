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

PASS_ON_VALUE = 2
NUM_TRIES = 1

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
  results_queue.put((request, 'do_not_recognize', None))


def pass_to_nearest_alive_node(message, successor):
  current_host_name = socket.getfqdn()

  if current_host_name in server_list:
    current_host_index = server_list.index(current_host_name)

  reply = None;

  index = current_host_index;

  while not reply:
    if successor:
      index = (index + 1) % len(server_list)
    else:
      index = (index - 1) % len(server_list)

    if index == current_host_index:
      break;

    next = (server_list[index], server_port);

    reply, address = sendRequest(message,next,None,NUM_TRIES);

  return reply, address


def add_node(request):
  global ring

  node_add = request['payload']
  
  ring.add_node(request['address'][0])

  data = None
  local_host_name = socket.getfqdn()

  if ring.node.host != node_add:

    message = assembleMessage(34, None, node_add)
    reply = pass_to_nearest_alive_node(message, True)

    ring.add_node(node_add)

    if request['address'][0] == node_add:
      request['address'] = list(request['address'])
      request['address'][1] = server_port
      request['address'] = tuple(request['address'])
      ring_list = ','.join(map(str, ring.ring.values()))
      results_queue.put((request, 'update_ring', ring_list))
    else:
      results_queue.put((request, 'success', None))

    transfer_keys(node_add)

def remove_node(request):
  global ring

  delete_node = request['payload']
  ring.add_node(request['address'][0])

  if ring.node.host != delete_node and (delete_node in ring.ring.values()):
    ring.remove_node(delete_node)

    results_queue.put((request, 'success', None))

    message = assembleMessage(38, None, delete_node)

    reply = pass_to_nearest_alive_node(message, False)
   

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

  results_queue.put((payload, forwarded_req_address[str(request['header'])]))

def update_ring(request):
  ring_list = request['payload'].split(',')
  ring.update_ring(ring_list)

def transfer_keys(node_add):
  new_node = ring.hash_key(node_add)
  for k in ring.node.data.keys():
    position = ring.get_node_position(request[k])[0]
    if position == new_node:
      message=assembleMessage(1,k,ring.node.data[k])
      sendRequest(message,(position,server_port),None,1)

def report_alive(request):
  results_queue.put((request,'alive', None))

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

def package_forward (raw_data, request):
  global forwarded_req_address
  forward = requestID(server_port)

  forwarded_req_address[str(forward)] = request['address']

  forward.append(struct.pack('<b',response_status['forwarded']))
  forward.extend(struct.pack('<h', len(rdata)))
  forward.extend(rdata)

  forward_str = "";
  for x in forward:
    forward_str = forward_str + struct.pack('<B', x)

  return forward_str

def routeMessage(raw_data, request):
  is_target = True
  if request['command'] in value_op:
    target_node = ring.get_node(request['key'])
    print target_node
    target_nodes = ring.get_node_with_replica(request['key'])
    print target_nodes
    if target_node != ring.node:
      is_target = False
      address = (target_node, server_port)
      forward_package = package_forward(raw_data, request)
      sock.sendto(forward_package, address)

  if is_target:
    task = Thread(target=operation, args=(request,))
    task.start()
    task.join()

def checkSuccessor():
  global ring

  local_host_name = socket.getfqdn()
  current_host_index = server_list.index(local_host_name)

  message = assembleMessage(33)
  reply, address = pass_to_nearest_alive_node(message, True)

  if reply:
    next_alive_index = server_list.index(socket.getfqdn(address[0]))

    ring.add_node(address[0]);

    transverse_index = next_alive_index - current_host_index;

    if transverse_index < 0:
      number_of_successive_nodes_dead = len(server_list) + transverse_index;
    else:
      number_of_successive_nodes_dead = transverse_index

    for index in range(1, number_of_successive_nodes_dead):
      i = (current_host_index+index) % len(server_list)
      dest_ip = socket.gethostbyname(server_list[i])
      msg = assembleMessage(38, None, dest_ip)
      ring.remove_node(dest_ip)
      rply = pass_to_nearest_alive_node(msg, False)
  else:
    ring.clear_ring()

  print ring.ring.values()


def initialize():
  global ring

  message = assembleMessage(34, None, ring.node.host)
  pass_to_nearest_alive_node(message, True)

def check_status():
  global check_status_time
  global operating
  while operating == True:
    checkSuccessor()
    time.sleep(check_status_time)

def reply_response():
  global results_queue
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

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("", 7790)
sock.bind(server_address)
operating = True

print "Listening on %s" % server_port

initialize()

status_check = Thread(target=check_status)
status_check.daemon =True
status_check.start()

status_check = Thread(target=reply_response)
status_check.daemon =True
status_check.start()

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