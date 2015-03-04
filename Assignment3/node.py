import md5

class Node(object):

	"""Initializes the Node Object"""
	def __init__(self):
    self.data = dict()

	def put(self,key,value):
    d = {key: value}
    self.data.update(d)
    return 'success', None

	def put_no_overwrite(self,key,value):
    if key not in self.data:
      put(key,value)
    else:
      return 'key_exist', None

	def get(self, key):
    if key in self.data:
      return 'success', self.data[key]
    else:
      return 'dne', None

	def remove(self,key):
    if key in self.data:
      self.data.pop(key, None)
      return 'success', None
    else:
      return 'dne', None

	def report_alive(self):
		raise NotImplementedError

	def report_update(self):
		raise NotImplementedError
	
	def check_alive(self):
		raise NotImplementedError