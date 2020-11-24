cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
curl -I localhost:8070 2> /dev/null | grep HTTP | diff - tests/localhost.out
kill $PID
