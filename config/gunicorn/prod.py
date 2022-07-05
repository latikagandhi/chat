"""Gunicorn *production* config file"""

import multiprocessing

# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "app:app"
# The number of worker processes for handling requests
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "eventlet"
# The socket to bind
bind = "0.0.0.0:5050"
# Write access and error info to /var/log
accesslog = "/var/log/gunicorn/chat_access.log"
errorlog = "/var/log/gunicorn/chat_error.log"
# Redirect stdout/stderr to log file
capture_output = True
# PID file so you can easily fetch process ID
pidfile = "/var/run/gunicorn/chat_prod.pid"
# Daemonize the Gunicorn process (detach & enter background)
daemon = True
