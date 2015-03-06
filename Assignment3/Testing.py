from communication import *
# Run the test cases and print out the result
def runTestCases(server_address):
    print "\n===============Integrity and Performance Testing===============\n"
    print server_address
    # Invalid Command
    try:
        print "Test Case: Invalid Command"
        data = sendRequest(assembleMessage(5,"0","123"), server_address,True)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 5
          print "\nPassed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"
    # Put - success case
    try:
        print "Test Case: put - success case"
        data = sendRequest(assembleMessage(1,"1","456"), server_address,True)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,"1",""), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == "456"
          print "\nPassed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"
    # Put - empty key
    try:
        print "Test Case: put - empty key"
        data = sendRequest(assembleMessage(1,"","/\\/\\/"), server_address,True)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,""), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == "/\\/\\/"
          print "\nPassed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"   
    # Put - empty value
    try:
        print "Test Case: put - empty value"
        data = sendRequest(assembleMessage(1,"P.;",""), server_address,True)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,"P.;"), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == ""
          print "\nPassed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"    
    # Put - existing key
    try:
        print "Test Case: put - existing key"
        data = sendRequest(assembleMessage(1,"1","123"), server_address)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 0
          sendRequest(assembleMessage(1,"1","{}'"), server_address,True)
          data = sendRequest(assembleMessage(2,"1"), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == "{}'"
          print "\nPassed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"    
    # Put - key with the maximum length
    try:
        print "Test Case: put - key with the maximum length"
        key = ""
        for i in range(0,32):
            key += '1'
        #print "Key to be sent: " + key
        data = sendRequest(assembleMessage(1,key,":lX"), server_address,True)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,key), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == ":lX"
          print "\nPassed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"        
    # Put - value with a very long length
    try:
        print "Test Case: put - value with the maximum length"
        value = ""
        for i in range(0,15000):
            value += '2'
        #print "Value to be sent: " + value
        data = sendRequest(assembleMessage(1,'\'MM\',`~-',value), server_address,True)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,'\'MM\',`~-'), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == value
          print "\nPassed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"            
    # Put without overwrite - success case
    try:
        print "Test Case: put without overwrite - success case"
        data = sendRequest(assembleMessage(3,"4"), server_address)
        if data:
          data = sendRequest(assembleMessage(32,"4","ab&"), server_address,True)
          res_code,payload = parsePayload(data)
          print "here1"
          assert res_code == 0
          data = sendRequest(assembleMessage(2,"4"), server_address)
          res_code,payload = parsePayload(data)
          print "here2"
          assert ''.join(payload) == "ab&"
          print "\nPassed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"    
    # Put without overwrite - empty key
    try:
        print "Test Case: put without overwrite - empty key"
        data = sendRequest(assembleMessage(3,""), server_address)
        if data:
          data = sendRequest(assembleMessage(32,"","..."), server_address,True)
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,""), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == "..."
          print "\nPassed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"       
    # Put without overwrite - empty value
    try:
        print "Test Case: put without overwrite - empty value"
        data = sendRequest(assembleMessage(3,"^"), server_address)
        if data:
          data = sendRequest(assembleMessage(32,"^",""), server_address,True)
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,"^"), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == ""
          print "\nPassed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"       
    # Put without overwrite - existing key
    try:
        print "Test Case: put without overwrite - existing key"
        data = sendRequest(assembleMessage(3,"0"), server_address)
        if data:
          data = sendRequest(assembleMessage(1,"0","4oop"), server_address)
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(32,"0","xp*"), server_address,True)
          res_code,payload = parsePayload(data)
          assert res_code == 32
          print "\nPassed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"       
    # Put without overwrite - key with the maximum length
    try:
        print "Test Case: put without overwrite - key with the maximum length"
        key = ""
        for i in range(0,32):
            key += '3'
        #print "Key to be sent: " + key
        data = sendRequest(assembleMessage(3,key), server_address)
        if data:
          data = sendRequest(assembleMessage(1,key,"ppp"), server_address,True)
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,key), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == "ppp"
          print "\nPassed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"            
    # Put without overwrite - value with a large length  
    try:
        print "Test Case: put without overwrite - value with the maximum length"
        value = ""
        for i in range(0,15000):
            value += '4'
        #print "Value to be sent: " + value
        data = sendRequest(assembleMessage(3,'\'M\fsdfdsfsdfdasfasff'), server_address)
        if data:
          data = sendRequest(assembleMessage(1,'\'M\fsdfdsfsdfdasfasff',value), server_address,True)
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,'\'M\fsdfdsfsdfdasfasff'), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == value
          print "\nPassed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"            
    # Get - non-existing key
    try:
        print "Test Case: get - non-existing key"
        sendRequest(assembleMessage(3,'f[pkpaksf\''), server_address)
        data = sendRequest(assembleMessage(2,"f[pkpaksf\'"), server_address,True)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 1
          print "\nPassed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"
    # Remove - success case
    try:
        print "Test Case: remove - success case"
        sendRequest(assembleMessage(1,'f[',"abc"), server_address)
        sendRequest(assembleMessage(3,"f["), server_address,True)
        data = sendRequest(assembleMessage(2,"f["), server_address)
        if data:
          res_code,payload = parsePayload(data)
          print res_code
          print ''.join(payload)
          assert res_code == 1
          print "\nPassed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"
    # Remove - non-existing (key,value)
    try:
        print "Test Case: remove - non-existing (key,value)"
        sendRequest(assembleMessage(3,'f++'), server_address)
        data = sendRequest(assembleMessage(3,"f++"), server_address,True)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 1
          print "\nPassed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"   
    # Remove - key with the maximum length
    try:
        print "Test Case: remove - key with the maximum length"
        key = ""
        for i in range(0,32):
            key += '*'
        #print "Key to be sent: " + key
        sendRequest(assembleMessage(1,key,":"), server_address)
        sendRequest(assembleMessage(3,key), server_address,True)
        data = sendRequest(assembleMessage(2,key), server_address)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 1
          print "\nPassed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"            
    # Out of Space error - Put 100001 (key,pair)
#     try:
#         print "Test Case: Out of Space"
#         key = ""
#         for i in range(0,100001):
#             sendRequest(assembleMessage(1,str(i),"abc"), server_address)
#         #print "Key to be sent: " + key
#         data = sendRequest(assembleMessage(1,"max",";;"), server_address,True)
#         if data:
#           res_code,payload = parsePayload(data)
#           assert res_code == 2
#           print "\nPassed\n"
#         else:
#             print "No response received."
#             assert False
#     except AssertionError:
#         print "\nFailed\n"            
    
#     # shutdown - success case
#     try:
#         data = sendRequest(assembleMessage(4), server_address,True)
#         if data:
#           res_code,payload = parsePayload(data)
#           assert res_code == 0
#           data = sendRequest(assembleMessage(1,"nnew","123"), server_address)
#           if data:
#               assert False
#           else:
#               print "\nPassed\n"
#         else:
#             print "No response received."
#             assert False
#     except AssertionError:
#         print "\nFailed\n"        