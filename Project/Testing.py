from communication import *
from time import strftime
# Run the test cases and print out the result
def runTestCases(server_address,file_object):
    file_object.write("===============Integrity and Performance Testing===============\n")
    file_object.write("Time:"+strftime("%Y-%m-%d %H:%M:%S")+"\n")
    print "\n===============Integrity and Performance Testing===============\n"
    file_object.write("Testing on "+server_address[0]+"\n")
    print server_address
    # Invalid Command
    try:
        file_object.write("Test Case: Invalid Command\n")
        print "Test Case: Invalid Command"
        data,address,turnAroundTime = sendRequest(assembleMessage(5,"0","123"), server_address,file_object)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 5
          file_object.write("\nPassed\n\n")
          print "\nPassed\n"
        else:
            file_object.write("No response received.\n")
            print "No response received."
            assert False
    except AssertionError:
        file_object.write("\nFailed\n\n")
        print "\nFailed\n"
    # Put - success case
    try:
        file_object.write("Test Case: put - success case\n")
        print "Test Case: put - success case"
        data,address,turnAroundTime = sendRequest(assembleMessage(1,"1","456"), server_address,file_object)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data,address,turnAroundTime = sendRequest(assembleMessage(2,"1",""), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == "456"
          file_object.write("\nPassed\n\n")
          print "\nPassed\n"
        else:
            file_object.write("No response received.\n")
            print "No response received."
            assert False
    except AssertionError:
        file_object.write("\nFailed\n\n")
        print "\nFailed\n"
    # Put - empty key
    try:
        file_object.write("Test Case: put - empty key\n")
        print "Test Case: put - empty key"
        data,address,turnAroundTime = sendRequest(assembleMessage(1,"","/\\/\\/"), server_address,file_object)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data,address,turnAroundTime = sendRequest(assembleMessage(2,""), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == "/\\/\\/"
          file_object.write("\nPassed\n\n")
          print "\nPassed\n"
        else:
            file_object.write("No response received.\n")
            print "No response received."
            assert False
    except AssertionError:
        file_object.write("\nFailed\n\n")
        print "\nFailed\n"   
    except TypeError:
        file_object.write("\nConnection Problem.\n")
        file_object.write("Failed\n\n")
        print "\nFailed\n"
    # Put - empty value
    try:
        file_object.write("Test Case: put - empty value\n")
        print "Test Case: put - empty value"
        data,address,turnAroundTime = sendRequest(assembleMessage(1,"P.;",""), server_address,file_object)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data,address,turnAroundTime = sendRequest(assembleMessage(2,"P.;"), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == ""
          file_object.write("\nPassed\n\n")
          print "\nPassed\n"
        else:
            file_object.write("No response received.\n")
            print "No response received."
            assert False
    except AssertionError:
        file_object.write("\nFailed\n\n")
        print "\nFailed\n"    
    # Put - existing key
    try:
        file_object.write("Test Case: put - existing key\n")
        print "Test Case: put - existing key"
        data,address,turnAroundTime = sendRequest(assembleMessage(1,"1","123"), server_address)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 0
          sendRequest(assembleMessage(1,"1","{}'"), server_address,file_object)
          data,address,turnAroundTime = sendRequest(assembleMessage(2,"1"), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == "{}'"
          file_object.write("\nPassed\n\n")
          print "\nPassed\n"
        else:
            file_object.write("No response received.\n")
            print "No response received."
            assert False
    except AssertionError:
        file_object.write("\nFailed\n\n")
        print "\nFailed\n"    
    except TypeError:
        file_object.write("\nConnection Problem.\n")
        file_object.write("Failed\n\n")
        print "\nFailed\n"
    # Put - key with the maximum length
    try:
        file_object.write("Test Case: put - key with the maximum length\n")
        print "Test Case: put - key with the maximum length"
        key = ""
        for i in range(0,32):
            key += '1'
        #print "Key to be sent: " + key
        data,address,turnAroundTime = sendRequest(assembleMessage(1,key,":lX"), server_address,file_object)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data,address,turnAroundTime = sendRequest(assembleMessage(2,key), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == ":lX"
          file_object.write("\nPassed\n\n")
          print "\nPassed\n"
        else:
            file_object.write("No response received.\n")
            print "No response received."
            assert False
    except AssertionError:
        file_object.write("\nFailed\n\n")
        print "\nFailed\n"        
#     # Put - value with the maximum length\
#     try:
#         file_object.write("Test Case: put - value with the maximum length\n")
#         print "Test Case: put - value with the maximum length"
#         value = ""
#         for i in range(0,15000):#15000
#             value += '2'
#         #print "Value to be sent: " + value
#         print "length:"+str(len(value))
#         data,address,turnAroundTime = sendRequest(assembleMessage(1,'111',value), server_address,file_object)
#         if data:
#           res_code,payload = parsePayload(data)
#           assert res_code == 0
#           data,address,turnAroundTime = sendRequest(assembleMessage(2,'111'), server_address)
#           res_code,payload = parsePayload(data)
#           assert ''.join(payload) == value
#           file_object.write("\nPassed\n\n")
#           print "\nPassed\n"
#         else:
#             file_object.write("No response received.\n")
#             print "No response received."
#             assert False
#     except AssertionError:
#         file_object.write("\nFailed\n\n")
#         print "\nFailed\n"   
                  
    # Put without overwrite - success case
    try:
        file_object.write("Test Case: put without overwrite - success case\n")
        print "Test Case: put without overwrite - success case"
        data,address,turnAroundTime = sendRequest(assembleMessage(3,"4"), server_address)
        if data:
          sendRequest(assembleMessage(32,"4","ab&"), server_address,file_object)
          data,address,turnAroundTime = sendRequest(assembleMessage(2,"4"), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == "ab&"
          file_object.write("\nPassed\n\n")
          print "\nPassed\n"
        else:
            file_object.write("No response received.\n")
            print "No response received."
            assert False
    except AssertionError:
        file_object.write("\nFailed\n\n")
        print "\nFailed\n"    
    # Put without overwrite - empty key
    try:
        file_object.write("Test Case: put without overwrite - empty key\n")
        print "Test Case: put without overwrite - empty key"
        data,address,turnAroundTime = sendRequest(assembleMessage(3,""), server_address)
        if data:
          data,address,turnAroundTime = sendRequest(assembleMessage(32,"","..."), server_address,file_object)
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data,address,turnAroundTime = sendRequest(assembleMessage(2,""), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == "..."
          file_object.write("\nPassed\n\n")
          print "\nPassed\n"
        else:
            file_object.write("No response received.\n")
            print "No response received."
            assert False
    except AssertionError:
        file_object.write("\nFailed\n\n")
        print "\nFailed\n"       
    # Put without overwrite - empty value
    try:
        file_object.write("Test Case: put without overwrite - empty value\n")
        print "Test Case: put without overwrite - empty value"
        data,address,turnAroundTime = sendRequest(assembleMessage(3,"^"), server_address)
        if data:
          data,address,turnAroundTime = sendRequest(assembleMessage(32,"^",""), server_address,file_object)
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data,address,turnAroundTime = sendRequest(assembleMessage(2,"^"), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == ""
          file_object.write("\nPassed\n\n")
          print "\nPassed\n"
        else:
            file_object.write("No response received.\n")
            print "No response received."
            assert False
    except AssertionError:
        file_object.write("\nFailed\n\n")
        print "\nFailed\n"       
    # Put without overwrite - existing key
    try:
        file_object.write("Test Case: put without overwrite - existing key\n")
        print "Test Case: put without overwrite - existing key"
        data,address,turnAroundTime = sendRequest(assembleMessage(3,"0"), server_address)
        if data:
          data,address,turnAroundTime = sendRequest(assembleMessage(1,"0","4oop"), server_address)
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data,address,turnAroundTime = sendRequest(assembleMessage(32,"0","xp*"), server_address,file_object)
          res_code,payload = parsePayload(data)
          assert res_code == 32
          file_object.write("\nPassed\n\n")
          print "\nPassed\n"
        else:
            file_object.write("No response received.\n")
            print "No response received."
            assert False
    except AssertionError:
        file_object.write("\nFailed\n\n")
        print "\nFailed\n"       
    # Put without overwrite - key with the maximum length
    try:
        file_object.write("Test Case: put without overwrite - key with the maximum length\n")
        print "Test Case: put without overwrite - key with the maximum length"
        key = ""
        for i in range(0,32):
            key += '3'
        #print "Key to be sent: " + key
        data,address,turnAroundTime = sendRequest(assembleMessage(3,key), server_address)
        if data:
          data,address,turnAroundTime = sendRequest(assembleMessage(1,key,"ppp"), server_address,file_object)
          res_code,payload = parsePayload(data)
          assert res_code == 0
          data,address,turnAroundTime = sendRequest(assembleMessage(2,key), server_address)
          res_code,payload = parsePayload(data)
          assert ''.join(payload) == "ppp"
          file_object.write("\nPassed\n\n")
          print "\nPassed\n"
        else:
            file_object.write("No response received.\n")
            print "No response received."
            assert False
    except AssertionError:
        file_object.write("\nFailed\n\n")
        print "\nFailed\n"            
#     # Put without overwrite - value with the maximum length
#     try:
#         file_object.write("Test Case: put without overwrite - value with the maximum length\n")
#         print "Test Case: put without overwrite - value with the maximum length"
#         value = ""
#         for i in range(0,15000):
#             value += '4'
#         #print "Value to be sent: " + value
#         data,address,turnAroundTime = sendRequest(assembleMessage(3,'\'M\fsdfdsfsdfdasfasff'), server_address)
#         if data:
#           data,address,turnAroundTime = sendRequest(assembleMessage(32,'\'M\fsdfdsfsdfdasfasff',value), server_address,file_object)
#           res_code,payload = parsePayload(data)
#           assert res_code == 0
#           data,address,turnAroundTime = sendRequest(assembleMessage(2,'\'M\fsdfdsfsdfdasfasff'), server_address)
#           res_code,payload = parsePayload(data)
#           assert ''.join(payload) == value
#           file_object.write("\nPassed\n\n")
#           print "\nPassed\n"
#         else:
#             file_object.write("No response received.\n")
#             print "No response received."
#             assert False
#     except AssertionError:
#         file_object.write("\nFailed\n\n")
#         print "\nFailed\n"            
    # Get - non-existing key
    try:
        file_object.write("Test Case: get - non-existing key\n")
        print "Test Case: get - non-existing key"
        sendRequest(assembleMessage(3,'f[pkpaksf\''), server_address)
        data,address,turnAroundTime = sendRequest(assembleMessage(2,"f[pkpaksf\'"), server_address,file_object)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 1
          file_object.write("\nPassed\n\n")
          print "\nPassed\n"
        else:
            file_object.write("No response received.\n")
            print "No response received."
            assert False
    except AssertionError:
        file_object.write("\nFailed\n\n")
        print "\nFailed\n"
    # Remove - success case
    try:
        file_object.write("Test Case: remove - success case\n")
        print "Test Case: remove - success case"
        sendRequest(assembleMessage(1,'f[',"abc"), server_address)
        sendRequest(assembleMessage(3,"f["), server_address,file_object)
        data,address,turnAroundTime = sendRequest(assembleMessage(2,"f["), server_address)
        if data:
          res_code,payload = parsePayload(data)
          print res_code
          print ''.join(payload)
          assert res_code == 1
          file_object.write("\nPassed\n\n")
          print "\nPassed\n"
        else:
            file_object.write("No response received.\n")
            print "No response received."
            assert False
    except AssertionError:
        file_object.write("\nFailed\n\n")
        print "\nFailed\n"
    # Remove - non-existing (key,value)
    try:
        file_object.write("Test Case: remove - non-existing (key,value)\n")
        print "Test Case: remove - non-existing (key,value)"
        sendRequest(assembleMessage(3,'f++'), server_address)
        data,address,turnAroundTime = sendRequest(assembleMessage(3,"f++"), server_address,file_object)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 1
          file_object.write("\nPassed\n\n")
          print "\nPassed\n"
        else:
            file_object.write("No response received.\n")
            print "No response received."
            assert False
    except AssertionError:
        file_object.write("\nFailed\n\n")
        print "\nFailed\n"   
    # Remove - key with the maximum length
    try:
        file_object.write("Test Case: remove - key with the maximum length\n")
        print "Test Case: remove - key with the maximum length"
        key = ""
        for i in range(0,32):
            key += '*'
        #print "Key to be sent: " + key
        sendRequest(assembleMessage(1,key,":"), server_address)
        sendRequest(assembleMessage(3,key), server_address,file_object)
        data,address,turnAroundTime = sendRequest(assembleMessage(2,key), server_address)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 1
          file_object.write("\nPassed\n\n")
          print "\nPassed\n"
        else:
            file_object.write("No response received.\n")
            print "No response received."
            assert False
    except AssertionError:
        file_object.write("\nFailed\n\n")
        print "\nFailed\n"            
    # Out of Space error - Put three key pairs [1998 pairs already existed]
    if server_address[0] == "planetlab2.csee.usf.edu":
        try:
             file_object.write("Test Case: Out of Space error - Put three key pairs\n")
             print "Test Case: Out of Space error - Put three key pairs"
             key = ""
    
             #print "Key to be sent: " + key
             data,address,turnAroundTime = sendRequest(assembleMessage(1,"max",";;"), server_address)
             if data:
               sendRequest(assembleMessage(1,"max2",";;"), server_address)
               data,address,turnAroundTime = sendRequest(assembleMessage(1,"max3",";;"), server_address,file_object)
               res_code,payload = parsePayload(data)
               assert res_code == 2
               file_object.write("\nPassed\n\n")
               print "\nPassed\n"
             else:
                 file_object.write("No response received.\n")
                 print "No response received."
                 assert False
        except AssertionError:
             file_object.write("\nFailed\n\n")
             print "\nFailed\n"            
       
     # shutdown - success case
    try:
         file_object.write("shutdown - success case\n")
         print "shutdown - success case"
         data,address,turnAroundTime = sendRequest(assembleMessage(4), server_address)
         if data:
            assert False
         else:
             print "No response received."
             data,address,turnAroundTime = sendRequest(assembleMessage(1,"max2223",",,,"), server_address)
             if data:
               assert False
             else:
               file_object.write("No response received.\n")
               file_object.write("\nPassed\n\n")
               print "\nPassed\n"
    except AssertionError:
         file_object.write("\nFailed\n\n")
         print "\nFailed\n"      
    print "Testing result is saved in testing_result.txt."  