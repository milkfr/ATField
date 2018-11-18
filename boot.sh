#!/bin/bash
#!/bin/bash
source venv/bin/activate
exec flask deploy

exec gunicorn wsgi:app -b 0.0.0.0:8080 -w 3 -k gevent --timeout 600 --access-logfile /tmp/gunicorn.access-MYDOMAIN.log --error-logfile /tmp/gunicorn.error-MYDOMAIN.log