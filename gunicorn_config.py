command = '/home/code/qwriter_web/env/bin/gunicorn'
pythonpath = '/home/code/qwriter_web/qwriter_web'
bind = '127.0.0.1:8001'
workers = 5
user = 'admin'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=qwriter_web.settings'
# loglevel = 'debug'
# accesslog = '/var/log/gunicorn/access_log_qwriter_web'
# acceslogformat ="%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
# errorlog =  '/var/log/gunicorn/error_log_qwriter_web'
