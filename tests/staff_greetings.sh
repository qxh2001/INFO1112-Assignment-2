cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
curl localhost:8070/greetings.html 2> /dev/null | diff - tests/staff_greetings.out
kill $PID
