import hashlib
import random

PASS_ON_VALUE = 2

server_list = ["planetlab1.cs.ubc.ca","plonk.cs.uwaterloo.ca","planetlab03.cs.washington.edu"]

class Ring(object):

  """Initializes the Ring Object"""
  def __init__(self, node):

    self.ring = dict()
    self.sorted_keys = []

    self.node = node

    self.add_node(node)

  def add_node(self, node):
    key = self.hash_key(node)
    self.ring[key] = node
    print self.ring
    self.sorted_keys.append(key)

    self.sorted_keys.sort()

  def remove_node(self, node):
    key = self.hash_key(node)
    del self.ring[key]
    self.sorted_keys.remove(key)

  def get_node(self, key_string):
    return self.get_node_position(string_key)[0]

  def get_node_position(self, key_string):
    if not self.ring:
      return None, None

    key = self.hash_key(key_string)
    print key

    nodes = self.sorted_keys

    for x in xrange(0, len(nodes)):
      node = nodes[x]

      if key <= node:
        return self.ring[node], x

    return self.ring[nodes[0]], 0

  def hash_key(self, key_string):
    m =  hashlib.sha224(key_string).hexdigest()
    return long(m, 16)

  def gossip(self, initialize=False):
    talk_to = random.sample(server_list, PASS_ON_VALUE)
    if not initialize:
      rand = random.random()
      if (rand < 1/len(server_list)):
        return True;
    else:
      status, value = report_alive()

  def intialization(self):
    self.gossip()