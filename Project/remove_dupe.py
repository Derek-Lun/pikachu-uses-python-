from sets import Set

outfile = open('outfile.txt', 'w')
server_list2 = Set(line.strip() for line in open('testnode.txt'))
server_list = Set(line.strip() for line in open('goodnodes2.txt'))
for server in server_list2:
  print server

servers = server_list2 - server_list

for server in servers:
  outfile.write("%s\n" % server)