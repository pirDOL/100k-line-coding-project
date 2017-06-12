import argparse
from multiprocessing import Process
import os
import string
import time
import random
import contextlib
import pymysql


@contextlib.contextmanager
def connect_database():
    conn = pymysql.connect(host='localhost', port=3306, user='root', db='test')
    try:
        yield conn
    finally:
        conn.close()


def prepare_database(n_query=0, n_feature_byte=65536):
    with connect_database() as conn:
        with conn.cursor() as cursor:
            cursor.execute('show tables like "norefusefeature"')
            if cursor.fetchone() is None:
                cursor.execute('create table norefusefeature (qid bigint unsigned NOT NULL, timestamp int NOT NULL, feature mediumblob NOT NULL, PRIMARY KEY(qid))ENGINE=InnoDB;')
            cursor.execute('truncate norefusefeature')
            if n_query != 0:
                sql = 'insert into norefusefeature(qid,timestamp,feature) values(%s,%s,%s)'
                values = []
                for i in range(n_query):
                    values.append((str(random.getrandbits(64)), str(int(time.time())), ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n_feature_byte))))
                cursor.executemany(sql, values)
        conn.commit()


def _insert_process(n_query, n_batch, n_feature_byte):
    with connect_database() as conn:
        sql = 'insert into norefusefeature(qid,timestamp,feature) values(%s,%s,%s)'
        values = []
        for i in range(n_query):
            values.append((str(random.getrandbits(64)), str(int(time.time())), ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n_feature_byte))))
        with conn.cursor() as cursor:
            i = 0
            while i < n_query:
                tm_trans = time.time()
                cursor.executemany(sql, values[i:i+n_batch])
                conn.commit()
                i += n_batch
                tm_trans = time.time() - tm_trans
                if tm_trans < 1:
                    time.sleep(1 - tm_trans)


def insert_process(n_query, n_batch, n_feature_byte):
    begin = time.time()
    conn = pymysql.connect(host='localhost', port=3306, user='root', db='test')
    cursor = conn.cursor()
    notice_log = 'tm_conn=%.2f' % (1000 * (time.time() - begin))
    begin = time.time()
    sql = 'insert into norefusefeature(qid,timestamp,feature) values(%s,%s,%s)'
    values = []
    for i in range(n_query):
        values.append((str(random.getrandbits(64)), str(int(time.time())), ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n_feature_byte))))
    notice_log += ' tm_buildsql=%.2f' % (1000 * (time.time() - begin))
     
    begin = time.time()
    i = 0
    tm_trans = 0
    while i < n_query:
        tm = time.time()
        cursor.executemany(sql, values[i:i+n_batch])
        conn.commit()
        i += n_batch
        tm = time.time() - tm
        tm_trans += tm
    notice_log += ' tm_insert=%.2f tm_trans=%.2f feature_byte=%d queries=%d qps=%.1f' % (1000 * (time.time() - begin), tm_trans * 1000, n_feature_byte, n_query, n_query / tm_trans)
    begin = time.time()
    cursor.close()
    conn.close()
    print '%s tm_clean=%.2f' % (notice_log, 1000 * (time.time() - begin))


def select_process(n_query, n_batch, n_feature_byte):
    begin = time.time()
    conn = pymysql.connect(host='localhost', port=3306, user='root', db='test')
    cursor = conn.cursor()
    notice_log = 'tm_conn=%.2f' % (1000 * (time.time() - begin))
    sql = 'select * from norefusefeature limit %d' % n_batch
     
    begin = time.time()
    i = 0
    records = 0
    while i < n_query:
        records += cursor.execute(sql)
        cursor.fetchmany(records)
        i += n_batch
    tm_select = time.time() - begin
    notice_log += ' tm_select=%.2f feature_byte=%d queries=%d records=%d qps=%.1f' % (1000 * tm_select, n_feature_byte, n_query / n_batch, records, n_query / tm_select)
    begin = time.time()
    cursor.close()
    conn.close()
    print '%s tm_clean=%.2f' % (notice_log, 1000 * (time.time() - begin))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--concurrency', type=int, default=10, help='#concurrency clients, default=10')
    parser.add_argument('-q', '--query', type=int, default=1000, help='#queries per client, default=1000')
    parser.add_argument('-b', '--batch', type=int, default=20, help='#queries per client, default=20')
    parser.add_argument('-f', '--feature', type=int, default=50 * 1024, help='#queries per client, default=50k')
    parser.add_argument('-r', '--reuse', action='store_true', help='not clean database before start')
    parser.add_argument('-v', '--version', action='store_true', help='show version')
    args = parser.parse_args()
    if args.version:
        print 'norefuse_mysql_benchmark version 1.0'
        return
     
    prepare_database(args.query, args.feature)
    client_process = []
    for i in range(args.concurrency):
        client_process.append(Process(target=insert_process, args=(args.query, args.batch, args.feature)))
        client_process.append(Process(target=select_process, args=(args.query, args.batch, args.feature)))
    for p in client_process:
        p.start()
    for p in client_process:
        p.join()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)