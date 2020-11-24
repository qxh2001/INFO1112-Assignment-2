cd ..
sleep 1
python3 webserv.py tests/empty_field_cfg.cfg | diff - tests/empty_field_cfg.out
