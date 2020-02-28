web: gunicorn github_monitor.wsgi
worker: celery -A github_monitor worker -c 1 -loglevel info
