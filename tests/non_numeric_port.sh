cd ..
sleep 1
python3 webserv.py tests/non_numeric_port.cfg | diff - tests/non_numeric_port.out
