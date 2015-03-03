from communication import *
# Run the test cases and print out the result
def runTestCases(server_address):
    # TEST CASES FOR INVALID FORMAT OF THE MESSAGE
    #
    #
    #
    # Invalid Command
    try:
        print "Test Case: Invalid Command"
        data = sendRequest(assembleMessage(5,"0","123"), server_address)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 5
          print "Passed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"
    # Put - success case
    try:
        print "Test Case: put - success case"
        data = sendRequest(assembleMessage(1,"1","456"), server_address)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,"1",""), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == "456"
          print "Passed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"
    # Put - empty key
    try:
        print "Test Case: put - empty key"
        data = sendRequest(assembleMessage(1,"","/\\/\\/"), server_address)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,"/\\/\\/"), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == ""
          print "Passed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"   
    # Put - empty value
    try:
        print "Test Case: put - empty value"
        data = sendRequest(assembleMessage(1,"P.;",""), server_address)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,"P.;"), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == ""
          print "Passed\n"
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
          data = sendRequest(assembleMessage(1,"1","{}'"), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == "{}'"
          print "Passed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"    
    # Put - key with a very large length
    try:
        print "Test Case: put - key with a very large length"
        key = ""
        for i in range(0,100000):
            key += '1'
        print "Key to be sent: " + key
        data = sendRequest(assembleMessage(1,key,":lX"), server_address)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,key), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == ":lX"
          print "Passed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"        
    # Put - value with a very long length
    try:
        print "Test Case: put - value with a very large length"
        value = ""
        for i in range(0,100000):
            value += '1'
        print "Value to be sent: " + value
        data = sendRequest(assembleMessage(1,'\'MM\',`~-',value), server_address)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,'\'MM\',`~-'), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == value
          print "Passed\n"
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
          data = sendRequest(assembleMessage(32,"4","ab&"), server_address)
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,"4"), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == "ab&"
          print "Passed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"    
    # Put without overwrite - empty key
    try:
        print "Test Case: put - empty value"
        data = sendRequest(assembleMessage(3,""), server_address)
        if data:
          data = sendRequest(assembleMessage(32,"","..."), server_address)
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,""), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == "..."
          print "Passed\n"
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
          data = sendRequest(assembleMessage(32,"^","88"), sever_address)
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,"^"), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == "88"
          print "Passed\n"
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
          data = sendRequest(assembleMessage(32,"0","xp*"), server_address)
          res_code,payload = parsePayload(data)
          assert res_code == 32
          print "Passed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"       
    # Put without overwrite - key with a very large length
    try:
        print "Test Case: put without overwrite - key with a very large length"
        key = ""
        for i in range(0,100000):
            key += '2'
        print "Key to be sent: " + key
        data = sendRequest(assembleMessage(3,key), server_address)
        if data:
          data = sendRequest(assembleMessage(1,key,"ppp"), server_address)
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,key), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == "ppp"
          print "Passed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"            
    # Put without overwrite - value with a very large length  
    try:
        print "Test Case: put - value with a very large length"
        value = ""
        for i in range(0,100000):
            value += '1'
        print "Value to be sent: " + value
        data = sendRequest(assembleMessage(3,'\'M\',`~-'), server_address)
        if data:
          data = sendRequest(assembleMessage(1,'\'M\',`~-',value), server_address)
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data = sendRequest(assembleMessage(2,'\'M\',`~-'), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == value
          print "Passed\n"
        else:
            print "No response received."
            assert False
    except AssertionError:
        print "\nFailed\n"            
    # Get - non-existing key

    # Remove - success case
    # Remove - non-existing (key,value)
    # Remove - key with a very large length
    # Out of Space error - Put 100001 (key,pair)
    # shutdown - success case