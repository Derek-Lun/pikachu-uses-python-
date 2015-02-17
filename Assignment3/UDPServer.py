import socket
import struct

data = {}

def put (request):
  print 'put'
  data.update(request['key'], request['value'])
  return 'success', None

def get (request):
  print 'get'
  if request['key'] in data:
    return 'success', data.get(request['key'])
  return 'dne', None 

def remove (request):
  print 'remove'
  if request['key'] in data:
    data.pop(request['key'], None)
    return 'success', None
  return 'dne', None 

def shutdown ():
  print 'shutdown'

command = {
  0 : put,
  1 : get,
  2 : remove,
  3 : shutdown
}

response_status = {
  'success': 0,
  'dne': 1,
  'oos': 2,
  'sys_overload': 3,
  'internal_failutre': 4,
  'do_not_recognize': 5
}

def parseCommand (recv):
  request = {}
  request['command'] = struct.unpack('<b',recv[16])
  request['command'] = request['command'][0]
  print (request['command'])
  request['key'] = recv[1:33]

  if request['command'] == 0:
    length = struct.unpack_from('<h', recv, 33)
    begin = 35
    request['value'] = recv[begin:begin+length]

  return request

def createReply (status, value = None):
  reply = bytearray()

  reply.append(struct.pack('<b',response_status[status]))

  if value:
    reply.extend(value)

  return reply  

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 7777)

sock.bind(server_address)

while True:
  print "Listening on %s" % server_address[1]

  rdata, address = sock.recvfrom(16384)

  req = parseCommand(rdata)

  if req['command'] in command:
    func = command[req['command']]
    value, status = func(req) 
    #sock.sentto(reply, address)
  else:
    print 'invalid command'
    reply = createReply('do_not_recognize')
    sock.sendto(reply, address)
    

