cd ..
sleep 1
python3 webserv.py tests/missing_field_cfg.cfg | diff - tests/missing_field_cfg.out