web: gunicorn --workers=3 --threads 3 qwriter_web.wsgi
release: python manage.py migrate --noinput && python manage.py compress --noinput && python manage.py collectstatic --noinput