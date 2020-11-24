cd ..
python3 webserv.py config.cfg &
PID=$!
sleep 1
python3 webserv.py invalid.cfg | diff - tests/no_cfg.out
kill $PID
