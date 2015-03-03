from communication import *
#Run the test cases and print out the result
def runTestCases(server_address):
    #TEST CASES FOR INVALID FORMAT OF THE MESSAGE
    #Invalid Command
    try:
        print "Test Case - Invalid Command"
        message=assembleMessage(5,"123","456")
        data = sendRequest(message, server_address)
        if data:
          res_code,payload = parsePayload(data)
          assert res_code == 5
          print "Passed - Invalid Command\n"
        else:
            assert False
    except AssertionError:
        print "\nFailed: Test Case - Invalid Command\n"
        #Put - success case
        #Put - empty value
        #Put - existing key
        #Put - key with a very large length
        #Put - value with a very large length
        #Put without overwrite - success case
        #Put without overwrite - empty value
        #Put without overwrite - existing key
        #Put without overwrite - key with a very large length
        #Put without overwrite - value with a very large length  
        #Get - success case
        #Get - non-existing key
        #Get - key with a very large length
        #Remove - success case
        #Remove - non-existing (key,value)
        #Remove - key with a very large length
        #Out of Space error - Put 100001 (key,pair)
        #shutdown - success case