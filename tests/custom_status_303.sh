cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
curl -I localhost:8070/cgibin/custom_status_303.py 2> /dev/null | grep HTTP | diff - tests/custom_status_303.out
kill $PID
