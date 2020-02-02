import multiprocessing

# 工作模式
worker_class = 'gevent'

# 并行工作进程数
workers = 4  # multiprocessing.cpu_count()

# 指定每个工作者的线程数
# threads = 2

# 监听地址
bind = '127.0.0.1:5000'

# 设置守护进程
daemon = 'false'

# 设置最大并发量
worker_connections = 10000

# 设置进程文件目录
# pidfile = '/var/run/gunicorn.pid'

# 设置访问日志和错误日志路径
accesslog = './logs/gunicorn_access.log'
errorlog = './logs/gunicorn_error.log'

# 设置日志记录水平
loglevel = 'warning'

# preload_app = True
