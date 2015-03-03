import md5

class Node(object):

	"""Initializes the Node Object"""
	def __init__(self):
		raise NotImplementedError

	def put(self,key,value):
		raise NotImplementedError

	def put_no_overwrite(self,key,value):
		raise NotImplementedError

	def get(self, key):
		raise NotImplementedError

	def remove(self,key):
		raise NotImplementedError

	def shutdown(self):
		raise NotImplementedError

	def report_alive(self):
		raise NotImplementedError

	def report_update(self):
		raise NotImplementedError
	
	def check_alive(self):
		raise NotImplementedError