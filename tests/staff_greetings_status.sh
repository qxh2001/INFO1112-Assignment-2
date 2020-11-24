cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
curl -I 127.0.0.1:8070/greetings.html 2> /dev/null | grep '200 OK' | diff - tests/staff_greetings_status.out
kill $PID
