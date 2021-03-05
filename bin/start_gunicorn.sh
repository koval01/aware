#!/bin/bash
source /home/code/qwriter_web/env/bin/activate
# source /home/www/code/project/env/bin/postactivate
exec gunicorn  -c "/home/code/qwriter_web/gunicorn_config.py" qwriter_web.wsgi
