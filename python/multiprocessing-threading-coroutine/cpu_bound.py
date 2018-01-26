#!/usr/bin/env python

from __future__ import print_function
from multiprocessing import dummy
import multiprocessing
import math
import random
import time
import gevent

def test(n_try):
    return sum(math.hypot(random.random(), random.random()) < 1 for _ in range(n_try))

def calculate_pi_single_thread(n_partition, n_try):
    begin = time.time()
    result = map(test, [n_try] * n_partition)
    pi = 4. * sum(result) / float(n_partition * n_try)
    print('single_thread tm=%d pi=%.7f' % (time.time() - begin, pi))

def calculate_pi_thread_pool(n_partition, n_try, n_thread):
    begin = time.time()
    p = dummy.Pool(n_thread)
    result = p.map(test, [n_try] * n_partition)
    pi = 4. * sum(result) / float(n_partition * n_try)
    print('thread_pool(%d) tm=%d pi=%.7f' % (n_thread, time.time() - begin, pi))

def calculate_pi_coroutine(n_partition, n_try):
    begin = time.time()
    jobs = [gevent.spawn(test, t) for t in [n_try] * n_partition]
    gevent.joinall(jobs, timeout=2)
    pi = 4. * sum([job.value for job in jobs]) / float(n_partition * n_try)
    print('coroutine tm=%d pi=%.7f' % (time.time() - begin, pi))   

def calculate_pi_process_pool(n_partition, n_try, n_process):
    begin = time.time()
    p = multiprocessing.Pool(n_process)
    result = p.map(test, [n_try] * n_partition)
    pi = 4. * sum(result) / float(n_partition * n_try)
    print('process_pool(%d) tm=%d pi=%.7f' % (n_process, time.time() - begin, pi))

if __name__ == '__main__':
    calculate_pi_single_thread(20000, 1000)
    calculate_pi_thread_pool(20000, 1000, 1)
    calculate_pi_thread_pool(20000, 1000, 10)
    calculate_pi_coroutine(20000, 1000)
    calculate_pi_process_pool(20000, 1000, 1)
    calculate_pi_process_pool(20000, 1000, 10)
