cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
curl localhost:8070/cgibin/bash_script_test.sh 2> /dev/null | diff - tests/bash_script.out
kill $PID
