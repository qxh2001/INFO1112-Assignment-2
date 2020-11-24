cd ..
sleep 1
python3 webserv.py tests/staff_missing_field.cfg | diff - tests/staff_missing_field.out
