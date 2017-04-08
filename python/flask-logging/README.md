## flask中logging使用

### 1 日志应用场景
基于flask开发的应用程序通常有三类日志，按照一次HTTP请求的处理顺序依次为：

2. url handler处理HTTP请求时打印的地址
3. handler使用的类的方法打印的日志
4. flask的web server打印的HTTP请求和响应日志

```python
@app.route('/')
def handler_home():
    logging.info('handler_home starts')
    u = Util()
    u.do_something()
    logging.info('handler_home ends')
    return 'hello world'

class Util(object):
    def do_something(self):
        logging.info('Util do_something')

INFO: 07-09 17:42:26: _internal.py:87 * 10348  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
INFO: 07-09 17:42:30: app.py:20 * 10348 handler_home starts
INFO: 07-09 17:42:30: app.py:16 * 10348 Util do_something
INFO: 07-09 17:42:30: app.py:23 * 10348 handler_home ends
INFO: 07-09 17:42:30: _internal.py:87 * 10348 127.0.0.1 - - [09/Jul/2016 17:42:30] "GET / HTTP/1
```

### 2 配置方法
在基于flask开发的应用中使用日志需要初始化两个logger：

1. flask的app对象自身有一个logger对象，它是用来打印HTTP请求响应日志，如果debug=True时还打印调试信息。这个日志是flask框架的内部代码自己打印的，业务代码不需要关心
2. 业务代码（包括handler以及自己写的类中打印的日志）使用logging模块的logger对象，通过logging.{warn,info,debug}等接口打印即可。位于单独的py文件中的类，import logging即可。

例：TimedRotatingFileHandler为定时自动切割，flask和业务代码的日志可以分别打印到不同的文件中，下面的设置是业务日志打印到app.log和app.log.wf中，flask的日志打印到access.log和access.log.wf中。
```python
import log
if __name__ == '__main__':
    log.init_log('./log/app.log')                       #初始化logging.logger
    log.init_log('./log/access.log', logger=app.logger) #初始化app.logger

# log.py
import os
import logging
import logging.handlers

def init_log(log_path, logger=None, level=logging.INFO, when="D", backup=7,
             format="%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s",
             datefmt="%m-%d %H:%M:%S"):
    """
    init_log - initialize log module

    Args:
      log_path      - Log file path prefix.
                      Log data will go to two files: log_path.log and log_path.log.wf
                      Any non-exist parent directories will be created automatically
      logger        - default using logging.getLogger()
      level         - msg above the level will be displayed
                      DEBUG < INFO < WARNING < ERROR < CRITICAL
                      the default value is logging.INFO
      when          - how to split the log file by time interval
                      'S' : Seconds
                      'M' : Minutes
                      'H' : Hours
                      'D' : Days
                      'W' : Week day
                      default value: 'D'
      format        - format of the log
                      default format:
                      %(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s
                      INFO: 12-09 18:02:42: log.py:40 * 139814749787872 HELLO WORLD
      backup        - how many backup file to keep
                      default value: 7

    Raises:
        OSError: fail to create log directories
        IOError: fail to open log file
    """
    formatter = logging.Formatter(format, datefmt)
    if not logger:
      logger = logging.getLogger()
    logger.setLevel(level)

    dir = os.path.dirname(log_path)
    if not os.path.isdir(dir):
        os.makedirs(dir)

    handler = logging.handlers.TimedRotatingFileHandler(log_path,
                                                        when=when,
                                                        backupCount=backup)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    handler = logging.handlers.TimedRotatingFileHandler(log_path + '.wf',
                                                        when=when,
                                                        backupCount=backup)
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
```

### 参考
1. [Flask logging not working at all](http://stackoverflow.com/questions/28925451/flask-logging-not-working-at-all)
1. [Using Flask and native Python logging?](http://stackoverflow.com/questions/31685075/using-flask-and-native-python-logging)
