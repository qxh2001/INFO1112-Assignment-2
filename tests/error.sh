cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
curl -I 127.0.0.1:8070/cgibin/error.py 2> /dev/null | grep HTTP | diff - tests/error.out
kill $PID
