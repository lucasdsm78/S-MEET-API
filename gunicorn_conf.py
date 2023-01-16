from multiprocessing import cpu_count

# Socket Path
bind = 'unix:/home/debian/smeet/gunicorn.sock'

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/home/debian/smeet/access_log'
errorlog =  '/home/debian/smeet/error_log'
