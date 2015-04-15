import socket
from communication import *
from Queue import Queue
import time
from threading import Thread
from threading import Timer
import json

server_port = 8889
alive_nodes = {}

child_port = 7790

NUM_TRIES = 1

results_queue = Queue()

server_list = [line.strip() for line in open('3node1.txt')]

print server_list

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

def output_log():
  global alive_nodes
  all_nodes = [line.strip() for line in open('3node1.txt')]
  # print "all nodes"
  # print all_nodes
  # print "alive nodes"
  # print alive_nodes
  nodes_status = []
  for node in all_nodes:
    temp_data = {}
    temp_data['hostname'] = node

    temp_data['alive'] = False
    if node in alive_nodes.keys():
      temp_data['alive'] = True
    # print "temp data"
    # print temp_data
    nodes_status.append(temp_data)

  log_file = open('../../var/www/html/3node1_log.json', 'w+')
  log_file.write(json.dumps(nodes_status))
  log_file.close()

def send_node_alive_info_to_other_nodes(request):
  for ip in alive_nodes.values():
    if ip != request['address'][0]:
      results_queue.put((request, 'alive', request['address'][0], ip))

def send_node_death_info_to_other_nodes(ip_address):
  output_log()
  message = assembleMessage(38, None, ip_address)
  data = addRequestID(message, child_port)
  for ip in alive_nodes.values():
    sock.sendto(data, (ip, child_port))

def initial_ring_update(request):
  for ip in alive_nodes.values():
    results_queue.put((request, 'alive', ip))

def node_is_alive(request, initial = True):
  global alive_nodes
  update = False
  hostname = socket.getfqdn(request['address'][0]).lower()
  ip_address = request['address'][0]

  if hostname in server_list:
    if ip_address not in alive_nodes.values():
      update = True
      send_node_alive_info_to_other_nodes(request)

    alive_nodes[hostname] = ip_address
    ring_list = ','.join(map(str, alive_nodes.values()))

    if update:
      output_log()

    if initial:
      initial_ring_update(request)

def node_is_dead(hostname):
  global alive_nodes

  ip_address = socket.gethostbyname(hostname)

  if (hostname in server_list) and (hostname in alive_nodes.keys()):
    del alive_nodes[hostname]

    send_node_death_info_to_other_nodes(ip_address)

command = {
  34 : node_is_alive
}

def no_operation(request):
  pass


def operation (request):
  try:
    command[request['command']](request)
  except:
    no_operation(request)

def parseCommand (recv, address):
  request = {}
  request['address'] = address

  try:
    request['header'] = recv[0:16]
    request['command'] = struct.unpack_from('<b',recv, 16)
    request['command'] = request['command'][0]

    length = struct.unpack_from('<h', recv, 16)
    begin = 19
    request['payload'] = recv[begin:begin+length[0]]

  except:
    request['command'] = no_operation

  return request

def createReply (request, status, value = None):
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

def reply_response():
  global results_queue
  while operating == True:
    if not results_queue.empty():
      result = results_queue.get()
      if len(result) > 2:
        reply = createReply(result[0], result[1], result[2])
        if len(result) > 3:
          sock.sendto(reply, (result[3], child_port))
        else:
          sock.sendto(reply, result[0]['address'])
      else:
        sock.sendto(result[0], result[1])

def check_status():
  global operating

  sleep_time = 60 / len(server_list)

  index = -1

  while operating == True:
    index = (index + 1) % len(server_list)
    time.sleep(sleep_time)

    message = assembleMessage(33)
    print "checking status of", server_list[index]
    node_address =  (server_list[index], child_port)
    reply, address = sendRequest(message,node_address,None,NUM_TRIES);

    if reply:
      print server_list[index], 'is alive'
      reply = parseCommand(reply, address)
      node_is_alive(reply, False)
    else:
      node_is_dead(server_list[index])


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("", server_port)
sock.bind(server_address)

print "Listening on %s" % server_port

operating = True

reply_thread = Thread(target=reply_response)
reply_thread.daemon =True
reply_thread.start()

status_check = Thread(target=check_status)
status_check.daemon =True
status_check.start()

while operating == True:
  try:
    rdata, address = sock.recvfrom(16384)

    req = parseCommand(rdata, address)
    print "Received: ",
    print req

    operation(req)

  except socket.error:
    #print "Socket closed"
    pass

sys.exit()