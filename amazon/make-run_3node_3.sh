ps -ef| grep "3node3_core.py" | grep "python" && echo "Running"
ps -ef| grep "3node3_core.py" | grep "python" || echo "Not Running" && python 3node3_core.py &
