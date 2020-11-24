cd ..
sleep 1
python3 webserv.py | diff - tests/staff_missing_arg.out
