cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
curl localhost:8070/ 2> /dev/null | diff - tests/root_to_index_html.out
kill $PID
