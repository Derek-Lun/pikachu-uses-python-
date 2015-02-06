import xmlrpclib
import operator

api_server = \
xmlrpclib.ServerProxy('https://www.planet-lab.org/PLCAPI/')

auth={}
auth['Username']="frhjing@interchange.ubc.ca"
# fill with your password
auth['AuthString']="fahrenheit4"
auth['AuthMethod']="password"

nodes = api_server.GetNodes(auth)

len(nodes)

hostnames = map(operator.itemgetter("hostname"), nodes)

f = open('listOfNodes.txt','w')

for host in hostnames:
	f.write(host + '\n')

f.close()
