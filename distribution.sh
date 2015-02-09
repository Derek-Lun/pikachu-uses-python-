file=$1
dfile=$2

echo "Starting Distribution"

echo ========================
cat ${file} | while read node
  do 
    echo ========================
    echo ${node}
    scp -i ~/.ssh/id_rsa ${dfile} ubc_eece411_5@${node}:~/.ssh/id_rsa
done