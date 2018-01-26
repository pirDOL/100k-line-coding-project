## python多进程、多线程、协程性能测试

### CPU密集型操作
单线程、只有一个线程的线程池、协程、单进程执行的时间都是9秒
多线程执行的时间是30秒
多进程执行的时间是6秒：测试的机器是双核，所以10个进程比1个进程，时间最多缩短一半
```
work@work-VirtualBox:~/ubuntu_share$ python cpu_bound.py 
single_thread tm=9 pi=3.1413056
thread_pool(1) tm=9 pi=3.1413062
thread_pool(10) tm=30 pi=3.1420796
coroutine tm=9 pi=3.1412004
process_pool(1) tm=9 pi=3.1415228
process_pool(10) tm=6 pi=3.1412360
```

### IO密集型操作
第一次测试协程和单线程的时间相同，这个不符合预期，重新安装gevent打平libevent版本后，协程耗时介于单线程和线程池之间。
```
work@work-VirtualBox:~/ubuntu_share$ python io_bound.py                            
io_bound.py:8: UserWarning: libevent version mismatch: system version is '2.0.21-st
able' but this gevent is compiled against '2.0.16-stable'
  import gevent
single_thread tm=8
thread_pool(4) tm=5
coroutine tm=8
process_pool(2) tm=5

work@work-VirtualBox:~/ubuntu_share$ python io_bound.py 
single_thread tm=28
thread_pool(4) tm=2
coroutine tm=9
process_pool(2) tm=4
```
