#!/bin/bash
cd /home/api
su -c 'gunicorn main.wsgi:application -b 0.0.0.0:10005 --log-level=debug --timeout=0 --access-logfile=-  --log-file=-' root