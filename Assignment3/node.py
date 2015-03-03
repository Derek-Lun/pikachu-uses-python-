import md5

class Node(object):

	"""Initializes the Node Object"""
	def __init__(self):
		raise NotImplementedError

	def report_alive(self):
		raise NotImplementedError

	def report_update(self):
		raise NotImplementedError
	
	def check_alive(self):
		raise NotImplementedError