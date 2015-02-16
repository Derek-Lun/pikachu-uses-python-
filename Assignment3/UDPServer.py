import socket
import sys
import array
import struct
import random
import time
import select

data = {}

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 7777)

sock.bind(server_address)

while True:
  print "Listening on %s" % server_address[1]

  data, address = sock.recvfrom(16384)