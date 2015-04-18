ps -ef| grep "3node2_core.py" | grep "python" && echo "Running"
ps -ef| grep "3node2_core.py" | grep "python" || echo "Not Running" && python 3node2_core.py &
