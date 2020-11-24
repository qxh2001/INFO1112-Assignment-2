cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
curl -I 127.0.0.1:8070/missing.html 2> /dev/null | grep '404' | diff - tests/staff_404_status.out
kill $PID
