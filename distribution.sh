file=$1

echo "Starting Distribution"

echo ========================
cat ${file} | while read node
do 
    echo ========================
    echo ${node}
    # ssh -n -i ~/.ssh/id_rsa -l ubc_eece411_5 ${node} "killall node; cd group10; node_modules/forever/bin/forever start server.js; exit"
    # scp -i ~/.ssh/id_rsa MonitoringNode/server.js ubc_eece411_5@${node}:group10/server.js
    scp -i ~/.ssh/id_rsa UDPServer.py ubc_eece411_5@${node}:Group10/.
    # ssh -n -i ~/.ssh/id_rsa -l ubc_eece411_5 ${node} "npm config set strict-ssl false; sudo chown -R $USER ~/.npm; sudo chown -R $USER /usr/local; npm install -g npm; cd group10; sudo chown -R $USER ~/.npm; npm install; npm install forever; node_modules/forever/bin/forever server.js; exit"
done


