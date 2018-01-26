#!/usr/bin/env python

from __future__ import print_function
from multiprocessing import dummy
import multiprocessing
import urllib2
import time
import gevent
import eventlet

def test(url):
    return len(urllib2.urlopen(url).read())

def test_patch(url):
    return len(eventlet.green.urllib2.urlopen(url).read())

def crawl(urls):
    begin = time.time()
    result = map(test, urls)
    print('single_thread tm=%d ret=%s' % (time.time() - begin, result))

    begin = time.time()
    p = dummy.Pool(4)
    result = p.map(test, urls)
    print('thread_pool(4) tm=%d ret=%s' % (time.time() - begin, result))

    begin = time.time()
    jobs = [gevent.spawn(test, url) for url in urls]
    gevent.joinall(jobs)
    print('coroutine_gevent tm=%d ret=%s' % (time.time() - begin, result))

    begin = time.time()
    p = eventlet.GreenPool()
    p.imap(test, urls)
    print('coroutine_eventlet(no patch) tm=%d ret=%s' % (time.time() - begin, result))
    
    begin = time.time()
    p = eventlet.GreenPool()
    p.imap(test_patch, urls)
    print('coroutine_eventlet(patch) tm=%d ret=%s' % (time.time() - begin, result))

    begin = time.time()
    p = multiprocessing.Pool(2)
    result = p.map(test, urls)
    print('process_pool(2) tm=%d ret=%s' % (time.time() - begin, result))

if __name__ == '__main__':
    crawl(['http://www.baidu.com', 'http://www.sina.com.cn', 'http://www.python.org'])
