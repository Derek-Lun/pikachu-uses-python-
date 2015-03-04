# from communication import *
# def runPerTestCases(server_address):
#     print "\n===============================Performance Test===============================\n"
#     print server_address
#     
#     print "Test: put"
#     data = sendRequest(assembleMessage(5,"0","123"), server_address,True)
#     if data:
#       res_code,payload = parsePayload(data)
#       if res_code == 0:
#         
#       else:
#         print "\nServer failure.\n"
#       
#     else:
#       print "\nNo response received.\n"