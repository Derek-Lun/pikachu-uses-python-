from threading import Thread
import subprocess
from Queue import Queue

import xmlrpclib
import operator

api_server = \
xmlrpclib.ServerProxy('https://www.planet-lab.org/PLCAPI/')

auth={}
# fill with your password
auth['Username']="frhjing@interchange.ubc.ca"
auth['AuthString']="#"
auth['AuthMethod']="password"

#nodes = api_server.GetNodes(auth)

#len(nodes)

#hostnames = map(operator.itemgetter("hostname"), nodes)

#------read from txt for now------------
#run getallNodes.py first and shorten the list for debugging
with open('listOfNodes.txt') as f:
    hostnames = f.readlines()
#---------------------------------------

num_threads = 4
queue = Queue()
#wraps system ping command
def pinger(i, q):
    """Pings subnet"""
    while True:
        ip = q.get()
        print "Thread %s: Pinging %s" % (i, ip)
        ret = subprocess.call("ping -n 1 %s" % ip,
            shell=True,
            stderr=subprocess.STDOUT)
        if ret == 0:
            print "%s: is alive" % ip
        else:
            print "%s: did not respond" % ip
        q.task_done()
#Spawn thread pool
for i in range(num_threads):

    worker = Thread(target=pinger, args=(i, queue))
    worker.setDaemon(True)
    worker.start()
#Place work in queue
for host in hostnames:
    queue.put(host)
#Wait until worker threads are done to exit    
queue.join()