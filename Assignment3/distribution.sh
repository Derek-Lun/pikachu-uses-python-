file=$1

echo "Starting Distribution"

echo ========================
cat ${file} | while read node
do 
    echo ========================
    echo ${node}
    ssh -n -i ~/.ssh/id_rsa -l ubc_eece411_5 ${node} "killall UDPServer; sudo rm -rf *; mkdir Group10"
    scp -i ~/.ssh/id_rsa ${file} ubc_eece411_5@${node}:node.txt
    scp -i ~/.ssh/id_rsa dist/UDPServer/* ubc_eece411_5@${node}:Group10/.
    scp -i ~/.ssh/id_rsa make-run.sh ubc_eece411_5@${node}:.
    ssh -n -i ~/.ssh/id_rsa -l ubc_eece411_5 ${node} "chmod +x ~/Group10/UDPServer; echo '*/5 * * * * sh make-run.sh' | sudo crontab; nohup Group10/UDPServer &"
done
