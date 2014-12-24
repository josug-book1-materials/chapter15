#!/bin/sh
echo 
echo "Usage : sh $0 <datacount>"
echo "This script insert data of the specified number and web response time 3 times."
echo "Notice: This script truncate current data and insert new data. "

echo "  <datacount>           : The number of data to insert."
echo "  env[MY_DB]  (required): DB Server address or hostname.    Use this to execute mysql command via ssh."
echo "  env[MY_LBS] (required): Load Balancer address or hostname.Use this to check resoponse time by curl command on 80 port"

echo "-- Check your patameter. --"
echo "[MY_DB]     = ${MY_DB}"
echo "[MY_LBS]    = ${MY_LBS}"
echo "<datacount> = ${1}"

echo "Press any key to continue or Ctrl-C to quit. :"
read 

echo "truncate contents;" |ssh ${MY_DB} mysql -u root sample_bbs
for i in `seq 1 ${1}`
do 
  echo "insert into contents values(null,now(),${i},null);"|ssh ${MY_DB} mysql -u root sample_bbs
done

echo -n "Data Count: "
echo "select count(*) as datacount from contents;"|ssh ${MY_DB} mysql -u root sample_bbs --skip-column-names

curl -L ${MY_LBS} -o /dev/null -w "response time(1): %{time_total}\n" 2> /dev/null
curl -L ${MY_LBS} -o /dev/null -w "response time(2): %{time_total}\n" 2> /dev/null
curl -L ${MY_LBS} -o /dev/null -w "response time(3): %{time_total}\n" 2> /dev/null

