file=$1

echo "Starting Distribution"

echo ========================
cat ${file} | while read node
do 
    echo ========================
    echo ${node}
    #ssh -n -i ~/.ssh/id_rsa -l ubc_eece411_5 ${node} "sudo yum groupinstall -y \"Development tools\";sudo yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel;mkdir ~/python;wget http://www.python.org/ftp/python/2.7.2/Python-2.7.2.tgz;tar zxfv Python-2.7.2.tgz;find ~/python -type d | xargs chmod 0755;cd Python-2.7.2;./configure;make;sudo make altinstall"

    ssh -n -i ~/.ssh/id_rsa -l ubc_eece411_5 ${node} "python2.7 -V;crontab -l; sudo /sbin/service crond start"
done
