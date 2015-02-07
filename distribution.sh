file=$1
dfile=$2

echo "Starting Distribution"

echo ========================
for node in `cat $file`
do
  echo ========================
  echo $node
  scp -i ~/.ssh/id_rsa $dfile ubc_eece411_5@$node:.
done