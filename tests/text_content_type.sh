cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
curl -I 127.0.0.1:8070/text.txt 2> /dev/null | grep 'Content-Type' | diff - tests/text_content_type.out
kill $PID
