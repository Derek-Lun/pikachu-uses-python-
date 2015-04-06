process="python2.7"
makerun=/home/ubc_eece411_5/Group10/UDPServer

pgrep "python2" && echo "Running"
pgrep $process || echo "Not Running" && python2.7 ~/Group10/UDPServer.py &
