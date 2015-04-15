ps -ef| grep "100node_core.py" | grep "python" && echo "Running"
ps -ef| grep "100node_core.py" | grep "python" || echo "Not Running" && python 100node_core.py &

ps -ef| grep "3node1_core.py" | grep "python" && echo "Running"
ps -ef| grep "3node1_core.py" | grep "python" || echo "Not Running" && python 3node1_core.py &

ps -ef| grep "3node2_core.py" | grep "python" && echo "Running"
ps -ef| grep "3node2_core.py" | grep "python" || echo "Not Running" && python 3node2_core.py &

ps -ef| grep "3node3_core.py" | grep "python" && echo "Running"
ps -ef| grep "3node3_core.py" | grep "python" || echo "Not Running" && python 3node3_core.py &
