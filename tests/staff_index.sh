cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
curl localhost:8070/ 2> /dev/null | diff - tests/staff_index.out
kill $PID
