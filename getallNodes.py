import xmlrpclib
import operator

api_server = \
xmlrpclib.ServerProxy('https://www.planet-lab.org/PLCAPI/')

auth={}
# change to your credentials
auth['Username']="frhjing@interchange.ubc.ca"
auth['AuthString']="#"
auth['AuthMethod']="password"

nodes = api_server.GetNodes(auth)

len(nodes)

hostnames = map(operator.itemgetter("hostname"), nodes)

f = open('listOfNodes.txt','w')

for host in hostnames:
	f.write(host + '\n')
	#print (host)

f.close()
