ps -ef| grep "3node1_core.py" | grep "python" && echo "Running"
ps -ef| grep "3node1_core.py" | grep "python" || echo "Not Running" && python 3node1_core.py &
