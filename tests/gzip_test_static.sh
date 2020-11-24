cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
curl -H "Accept-Encoding: gzip" -s 127.0.0.1:8070/index.html
gunzip -c temp.txt.gz | diff - tests/gzip_test_static.out
kill $PID
