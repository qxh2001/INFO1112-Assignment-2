cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
curl -I localhost:8070/cgibin/python_content_type.py 2> /dev/null | grep Content-Type | diff - tests/python_content_type.out
kill $PID
