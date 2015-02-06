import xmlrpclib
import operator

api_server = \
xmlrpclib.ServerProxy('https://www.planet-lab.org/PLCAPI/')

auth={}
# change to your credentials
auth['Username']="frhjing@interchange.ubc.ca"
auth['AuthString']="#"
auth['AuthMethod']="password"

f = open('listOfNodes.txt','r')

nodelist = []

for line in f:
  nodelist.append(line.rstrip());

print "adding Slice to " + str(len(nodelist)) + " nodes"
api_server.AddSliceToNodes(auth, 'ubc_eece411_5',nodelist);
print "finished adding Slice to " + str(len(nodelist)) + " nodes"
