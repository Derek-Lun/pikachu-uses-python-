import socket
import sys
import array
import struct
import random
import time
import select

data = {}


def parseCommand (recv):
  request = {}
  request['command'] = recv[:1]
  request['key'] = recv[1:33]

  if request['command'] == struct.pack('<B', 1):
    length = struct.unpack_from('<h', recv, 33)
    begin = 35
    request['value'] = recv[begin:being+length]

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 7777)

sock.bind(server_address)

while True:
  print "Listening on %s" % server_address[1]

  data, address = sock.recvfrom(16384)

  req = parseCommand(data)



