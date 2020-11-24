cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
python3 webserv.py invalid | diff - tests/staff_invalid_path.out
kill $PID
