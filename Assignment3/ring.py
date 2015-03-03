import md5

class Ring(object):

	"""Initializes the Ring Object"""
	def __init__(self, nodes=None):

		self.ring = dict()
		self.sorted_keys = []

	def add_node(self, node):
		raise NotImplementedError

	def remove_node(self, node):
		raise NotImplementedError

	def get_node(self, key_string):
		raise NotImplementedError

	def get_node_position(self, key_string):
		raise NotImplementedError

	def hash_key(self, key_string):
		raise NotImplementedError
