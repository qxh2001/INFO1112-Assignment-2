cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
curl localhost:8070/cgibin/hello.py 2> /dev/null | diff - tests/staff_cgibin_hello.out
kill $PID
