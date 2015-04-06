import sys

from Testing import runTestCases
from communication import *

servers = ["localhost","planetlab1.cs.ubc.ca","plonk.cs.uwaterloo.ca","cs-planetlab3.cs.surrey.sfu.ca","planet1.pnl.nitech.ac.jp","planetlab1.dojima.wide.ad.jp","planetlab4.goto.info.waseda.ac.jp","planetlab1.csg.uzh.ch","icnalplabs2.epfl.ch","icnalplabs1.epfl.ch","plab4.ple.silweb.pl","ple2.dmcs.p.lodz.pl","planetlab4.mini.pw.edu.pl","planetlab3.net.in.tum.de","planetlab01.tkn.tu-berlin.de","planetlab2.informatik.uni-erlangen.de","planetlab1.tlm.unavarra.es","planetlab1.upc.es","planetlab3.upc.es","planetlab2.csee.usf.edu","host2.planetlab.informatik.tu-darmstadt.de","pl1.tailab.eu","pl-node-1.csl.sri.com","onelab3.info.ucl.ac.be","planetlab1.xeno.cl.cam.ac.uk","planetlab2.tamu.edu","pl2.tailab.eu","planetlab-03.cs.princeton.edu","planetlab-coffee.ait.ie","ple2.tu.koszalin.pl","aguila2.lsi.upc.edu","planetlab1.cs.uml.edu","planetlab2.acis.ufl.edu","aguila1.lsi.upc.edu","planet-lab1.cs.ucr.edu","planetlab1.csuohio.edu","plab1.cs.msu.ru","pl2.cs.unm.edu","kc-sce-plab2.umkc.edu","planetlab2.cs.purdue.edu","planetlab2.koganei.itrc.net","planetlab1.koganei.itrc.net","planetlab2.cs.umass.edu","ricepl-2.cs.rice.edu","planetlab-n1.wand.net.nz","75-130-96-13.static.oxfr.ma.charter.com","planetlab2.informatik.uni-kl.de","planetlab1.informatik.uni-kl.de","planetlab3.cesnet.cz","planetlab1.unr.edu","planetlab1.acis.ufl.edu","planetlab2.cis.upenn.edu","pl3.cs.unm.edu","planetlab1.postel.org","pli1-pa-1.hpl.hp.com","planetlab1.net.in.tum.de","planetlab6.csee.usf.edu","pl2.pku.edu.cn","planetlab2.citadel.edu","planetvs2.informatik.uni-stuttgart.de","planetlab-2.scie.uestc.edu.cn","pli1-pa-3.hpl.hp.com","planetlab1.tmit.bme.hu","planetlab-2.fhi-fokus.de","peeramidion.irisa.fr","planetlab2.netlab.uky.edu","planetlab1.cs.uiuc.edu","planetlab-um00.di.uminho.pt","planetlab-n2.wand.net.nz"]
#servers_representative = ["planetlab1.cs.ubc.ca"]
servers_representative = ["planetlab1.cs.ubc.ca","plonk.cs.uwaterloo.ca","cs-planetlab3.cs.surrey.sfu.ca"]

#server_address = ( servers[0] , 7790)

operating = True;
while operating == True:
    print "1: Manual Input 2: Testing (This will shutdown the server.) 3:Close Client"
    input = raw_input()
    if input == '1' :
        for i in range(len(servers)):
            print str(i)+':'+servers[i]
        print "Enter the index of a server:"
        server_chosen = int(raw_input())
        if server_chosen not in range(0,121):
            print "Invalid input."
        else:
            print "Connecting to "+servers[server_chosen]+"..."
            server_address = (servers[server_chosen],7790)
            print "Enter the command (1:put 2:get 3:remove 4:shutdown 32:put without overwrite, 33: ping, 34: addnode):"
            command = int(raw_input())
            key = None
            value = None
            if command == 4:
                print "Shutting down the server..."
            elif command in (33,34):
                print "temporary commands only"
            else:
                print "Enter the key:"
                key = raw_input()
                if command in (1,32):
                    print "Enter the value:"
                    value = raw_input()
            
            #Assemble a sending message
            message=assembleMessage(command,key,value)
                
            data,server = sendRequest(message, server_address)
            
            if data:
              parsePayload(data)
    elif input == '2':
        # Testing on all the servers
        fo = open("testing_result.txt", "w+")
        runTestCases(servers_representative,fo)
        fo.close()
    elif input == '3':
        operating = False;
        print "Shutting down client..."
    else:
        print "Invalid input."

