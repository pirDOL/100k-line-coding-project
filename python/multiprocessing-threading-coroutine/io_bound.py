#!/usr/bin/env python

from __future__ import print_function
from multiprocessing import dummy
import multiprocessing
import urllib2
import time
import gevent

def test(url):
    return urllib2.urlopen(url).read()

def crawl(urls):
    begin = time.time()
    result = map(test, urls)
    print('single_thread tm=%d' % time.time() - begin)

    begin = time.time()
    p = dummy.Pool(3)
    result = p.map(test, urls)
    print('thread_pool(3) tm=%d' % time.time() - begin)

    begin = time.time()
    jobs = [gevent.spawn(test, url) for url in urls]
    gevent.joinall(jobs)
    print('coroutine tm=%d' % time.time() - begin)

    begin = time.time()
    p = multiprocessing.Pool(3)
    result = p.map(test, urls)
    print('process_pool(3) tm=%d' % time.time() - begin)

if __name__ == '__main__':
    crawl(['http://www.baidu.com', 'http://www.sina.com.cn', 'http://www.python.org'])
