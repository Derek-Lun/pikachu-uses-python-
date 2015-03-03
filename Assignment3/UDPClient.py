import sys

from PerformanceTest import runTestCases
from communication import *

servers = ["localhost","planetlab1.cs.ubc.ca ","pllab1.kamgu.ru","pli1-br-2.hpl.hp.com","pllab2.kamgu.ru","planetlab5.cs.duke.edu","planetlab-2.rml.ryerson.ca","planetlab2.aub.edu.lb","planetlab1.aub.edu.lb","planetlab-1.vuse.vanderbilt.edu","planetlab2.iin-bit.com.cn","planetlab2.olsztyn.rd.tp.pl","pl2.bit.uoit.ca","planetlab-1.rml.ryerson.ca","planetlab2.cs.unb.ca","planetlab1.engr.ccny.cuny.edu","planet-lab.iki.rssi.ru","plab2.psgtech.ac.in","planetlab1.cs.unb.ca","itchy.cs.uga.edu","scratchy.cs.uga.edu","planetlab2.engr.ccny.cuny.edu","planetlab1.nowogrodzka.rd.tp.pl","planetlab2.iitr.ernet.in","planetlab0.ias.csusb.edu","pl1.bit.uoit.ca","planetlab2.cse.msu.edu","node0.planetlab.etl.luc.edu","mnc2.pusan.ac.kr","pl2.ernet.in","planetlab1.cs.wayne.edu","planetlab2.cse.nd.edu","charon.cs.binghamton.edu","planetlab1.homelinux.org","planetlab-2.vuse.vanderbilt.edu","node1.planetlab.etl.luc.edu","planetlab2.iitb.ac.in","planetlab1.iitb.ac.in","planetlab1.iin-bit.com.cn","planetlab2.cs.duke.edu","pl2.cewit.stonybrook.edu","pl1.cewit.stonybrook.edu","planetlab2.nileu.edu.eg","planetlab1.nileu.edu.eg","planetlabnode-1.docomolabs-usa.com","planetlab1.simula.no","planetlabnode-2.docomolabs-usa.com","pluto.cs.binghamton.edu","planetlab2.pop-ce.rnp.br","planetlab1.pop-ce.rnp.br","planetlab1.lublin.rd.tp.pl","planetlab2.csee.usf.edu","planetlab1.gdansk.rd.tp.pl","planetlab2.csg.uzh.ch","pl1.tailab.eu","planetlab2.ionio.gr","planetlab3.canterbury.ac.nz","pl-node-1.csl.sri.com","onelab3.info.ucl.ac.be","ricepl-1.cs.rice.edu","planetlab1.xeno.cl.cam.ac.uk","planetlab-4.eecs.cwru.edu","peeramide.irisa.fr","planetlab01.tkn.tu-berlin.de","planetlab-2.cs.auckland.ac.nz","planetlab3.postel.org","pl3.sos.info.hiroshima-cu.ac.jp","planetlab-2.sysu.edu.cn","pl2.tailab.eu","csplanetlab3.kaist.ac.kr","planetlab4.wail.wisc.edu","icnalplabs2.epfl.ch","plab-2.sinp.msu.ru","planetlab7.millennium.berkeley.edu","icnalplabs1.epfl.ch","planetlab-03.cs.princeton.edu","planetlab-13.e5.ijs.si","planetlab-coffee.ait.ie","ple2.tu.koszalin.pl","pl2.eecs.utk.edu","planetlab4.canterbury.ac.nz","planetlab1.sics.se","planet-lab4.uba.ar","aguila2.lsi.upc.edu","planck249ple.test.iminds.be","planck250ple.test.iminds.be","planetlab1.cs.uml.edu","plan1.project.cwi.nl","planetlab3.di.unito.it","planetlab2.buaa.edu.cn","planetlab-02.kusa.ac.jp","planetlab2.acis.ufl.edu","planetx.scs.cs.nyu.edu","aguila1.lsi.upc.edu","planetlab1.hust.edu.cn","planetlab1.iii.u-tokyo.ac.jp","planetlab-2.usask.ca","planet-lab1.cs.ucr.edu","planetlab4.eecs.umich.edu","earth.cs.brown.edu","planetlab1.cs.pitt.edu","planetlab2.cnds.jhu.edu","planetlab1.csuohio.edu","plab1.cs.msu.ru","roam2.cs.ou.edu","planet-lab2.ufabc.edu.br","pl2.cs.unm.edu","kc-sce-plab2.umkc.edu","planetlab-1.cmcl.cs.cmu.edu","planetlab-3.cmcl.cs.cmu.edu","plab1.nec-labs.com","plonk.cs.uwaterloo.ca","planetlab2.cs.purdue.edu","pl-dccd-02.cua.uam.mx","planetlab7.csres.utexas.edu","planet-plc-3.mpi-sws.org","planetlab1.inf.ethz.ch","planetlab3.singaren.net.sg","planetlab2.cs.uiuc.edu","planetlab5.csail.mit.edu","planetlab2.csie.nuk.edu.tw"]

server_address = ( servers[0] , 7790)

operating = True;
while operating == True:
    print "1: User Input 2: Performance Testing 3:Close Client"
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
            print "Enter the command (1:put 2:get 3:remove 4:shutdown 32:put without overwrite):"
            command = int(raw_input())
            if command in (1,2,3,4,32):
                if command == 4:
                    print "Shutting down the server..."
                else:
                    print "Enter the key:"
                    key = raw_input()
                    if command == 1:
                        print "Enter the value:"
                        value = raw_input()
                
                #Assemble a sending message
                message=assembleMessage(command,key,value)
                    
                data = sendRequest(message, server_address)
                
                if data:
                  res_code,payload = parsePayload(data)
                
                  print ''.join(payload);
            else:
                print "Error: Invalid command. (1:put 2:get 3:remove 4:shutdown 32:put without overwrite)"
    elif input == '2':
        runTestCases((servers[0], 7790));
    elif input == '3':
        operating = False;
        print "Shutting down client..."
    else:
        print "Invalid input."

