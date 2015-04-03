import hashlib

class Ring(object):

  """Initializes the Ring Object"""
  def __init__(self, node, port):

    self.ring = dict()
    self.sorted_keys = []

    self.node = node
    self.server_port = port

    self.add_node(node.host)

  def add_node(self, node):
    key = self.hash_key(node)
    self.ring[key] = node

    if not key in self.sorted_keys:
      self.sorted_keys.append(key)

    self.sorted_keys.sort()

  def remove_node(self, node):
    if node in self.ring.values():
      key = self.hash_key(node)
      del self.ring[key]
      self.sorted_keys.remove(key)

  def update_ring(self, nodes):
    del self.sorted_keys[:]
    for n in nodes:
      self.add_node(n)

  def clear_ring(self):
    self.ring.clear()
    del self.sorted_keys[:]

    self.add_node(self.node.host)

  def get_node(self, key_string):
    return self.get_node_position(key_string)[0]

  def get_node_position(self, key_string):
    if not self.ring:
      return None, None

    key = self.hash_key(key_string)

    nodes = self.sorted_keys

    for x in xrange(0, len(nodes)):
      node = nodes[x]

      if key <= node:
        return self.ring[node], x

    return self.ring[nodes[0]], 0

  def get_node_with_replica(self, key_string, replica=3):
    primary_node, index = self.get_node_position(key_string)

    node_placement = []

    for x in range(replica):
      i = (index + x) % len(self.sorted_keys);
      print i
      print len(self.sorted_keys)
      node = self.sorted_keys[i]
      node_placement.append(self.ring[node])

    return node_placement

  def hash_key(self, key_string):
    m =  hashlib.md5(key_string).hexdigest()

    return long(m, 16)

