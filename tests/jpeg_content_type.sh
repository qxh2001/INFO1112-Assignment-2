cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
curl -I 127.0.0.1:8070/tanjiro.jpeg 2> /dev/null | grep 'Content-Type' | diff - tests/jpeg_content_type.out
kill $PID
