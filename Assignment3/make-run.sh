process="UDPServer"
makerun=/home/ubc_eece411_5/Group10/UDPServer

pgrep $process && echo "Running"
pgrep $process || echo "Not Running" && nohup ~/Group10/UDPServer &
