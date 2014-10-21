export JAVA_OPTS="-Durl=${GAT_SCHEME}://${GAT_HOST}${GAT_PATH} -Drepeat=${GAT_RPT} -Duser=${GAT_USER} -Dduration=${GAT_DUR} -Dname=${GAT_NAME}"
TESTNAME=${GAT_NAME}_u${GAT_USER}_r${GAT_RPT}_s${GAT_DUR}
RF=/usr/share/nginx/html/gatling/
mkdir -p ${RF}
echo "${TESTNAME} start."
bin/gatling.sh -s SampleAppGet -rf ${RF} -on ${TESTNAME}
