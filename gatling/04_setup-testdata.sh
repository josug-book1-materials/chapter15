#!/bin/sh

echo "truncate contents;" |ssh ${MY_DB} mysql -u root sample_bbs
for i in `seq 1 ${1}`
do 
  echo "insert into contents values(null,now(),${i},null);"|ssh ${MY_DB} mysql -u root sample_bbs
done

echo "select count(*) from contents;"|ssh ${MY_DB} mysql -u root sample_bbs

curl -L ${MY_LBS} -o /dev/null -w "response: %{time_total}\n" 2> /dev/null
curl -L ${MY_LBS} -o /dev/null -w "response: %{time_total}\n" 2> /dev/null
curl -L ${MY_LBS} -o /dev/null -w "response: %{time_total}\n" 2> /dev/null

echo
