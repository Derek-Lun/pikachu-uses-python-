from sets import Set

server_list = list(line.strip() for line in open('100node.txt'))
server_list.sort()

outfile = open('100node.txt', 'r+')

for server in server_list:
  outfile.write("%s:7790\n" % server)