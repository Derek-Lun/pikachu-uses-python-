import hashlib

class Ring(object):

  """Initializes the Ring Object"""
  def __init__(self, node, port):

    self.ring = dict()
    self.sorted_keys = []

    self.node = node
    self.server_port = port

    self.add_node(node)

  def add_node(self, node):
    key = self.hash_key(node)
    self.ring[key] = node
    self.sorted_keys.append(key)

    self.sorted_keys.sort()

  def remove_node(self, node):
    key = self.hash_key(node)
    del self.ring[key]
    self.sorted_keys.remove(key)

  def update_ring(self, nodes):
    del self.sorted_keys[:]
    for n in nodes:
      self.add_node(n)

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

