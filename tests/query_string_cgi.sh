cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
(curl localhost:8070/cgibin/hello.py?name=Katherine&age=19) 2> /dev/null | diff - tests/query_string_cgi.out
kill $PID
