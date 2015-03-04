import md5

class Node(object):

  """Initializes the Node Object"""
  def __init__(self, ip_string, port):
    self.data = dict()
    self.host = ip_string
    self.port = port

  def put(self, key, value):
    print 'Operation: put'
    d = {key: value}
    self.data.update(d)
    return 'success', None

  def put_no_overwrite(self, key, value):
    print 'Operation: put without overwrite'
    if key not in self.data:
      put(key,value)
    else:
      return 'key_exist', None

  def get(self, key, value=None):
    print 'Operation: get'
    if key in self.data:
      return 'success', self.data[key]
    else:
      return 'dne', None

  def remove(self,key, value=None):
    print 'Operation: remove'
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