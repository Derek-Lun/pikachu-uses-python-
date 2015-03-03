import sys

from performanceTest import runTestCases
from communication import *

server_address = ( 'localhost' , 7790)

operating = True;
while operating == True:
    print "1: User Input 2: Performance Testing 3:Close Client"
    input = raw_input()
    if input == '1' :
        print "Enter the command (1:put 2:get 3:remove 4:shutdown 32:put without overwrite):"
        command = int(raw_input())
        if(command in (1,2,3,4,32)):
            if command == 4:
                print "Shutting down the server..."
            else:
                print "Enter the key:"
                key = raw_input()
                if command == 1:
                    print "Enter the value:"
                    value = raw_input()
                else:
                    value = None
            
            #Assemble a sending message
            message=assembleMessage(command,key,value)
                
            data = sendRequest(message, server_address)
            
            if data:
              res_code,payload = parsePayload(data)
            
              print ''.join(payload);
        
            
        else:
            print "Error: Invalid command. (1:put 2:get 3:remove 4:shutdown 32:put without overwrite)"
    elif input == '2':
        runTestCases(server_address);
    elif input == '3':
        operating = False;
        print "Shutting down client..."
    else:
        print "Invalid input."

