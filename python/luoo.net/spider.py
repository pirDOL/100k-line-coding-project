#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: spider.py
Author: pirdol@qq.com
Date: 2017/03/19 20:35:00
Description: crawl volumn from luoo.net
'''

from __future__ import print_function

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import shutil
import os
import json
import os.path
import random
import urlparse
import argparse
from multiprocessing import Process
from multiprocessing import Queue

import requests
from bs4 import BeautifulSoup

class CrawlProcess(Process):
	def __init__(self, http_proxy_list, baseurl, volumn_number_list, volumn_description_filepath, download_queue):
		super(CrawlProcess, self).__init__() # same as Process.__init__(self)
		self._baseurl = baseurl
		self._http_proxy_list = http_proxy_list
		self._volumn_number_list = volumn_number_list
		self._download_queue = download_queue
		self._volumn_description_filepath = volumn_description_filepath

	def run(self):
		for volumn_number in self._volumn_number_list:
			volumn_html = self._crawl_volumn(urlparse.urljoin(self._baseurl, volumn_number))
			if volumn_html is None:
				sys.stderr.write('crawl failed, volumn_number[%s]', volumn_number)
				continue

			volumn_description = self._parse_volumn(volumn_html)
			if volumn_description is None:
				sys.stderr.write('parse failed, volumn_number[%s]', volumn_number)
				continue

			self._download_queue.put(self._convert_volumn_description_to_download_info(volumn_description))
			self._write_volumn_description_file(volumn_description)

	def _crawl_volumn(self, volumn_url):
		if self._http_proxy_list == []:
			return requests.get(volumn_url).content
		else:
			return requests.get(volumn_url, proxies=self._select_proxy()).content

	def _select_proxy(self):
		return {'http': random.choice(self._http_proxy_list)}

	def _parse_track(self, track_html_list):
		track_list = []
		for track_html in track_html_list:
			parsed_track_html = BeautifulSoup(track_html, 'html.parser')
			track_list.append({
				'trackname': parsed_track_html.find('a', attrs={'class': 'trackname'}).text,
				'artist': parsed_track_html.find('span', attrs={'class': 'artist'}).text
			})
		return track_list

	def _parse_volumn(self, volumn_html):
		parsed_volumn_html = BeautifulSoup(volumn_html, 'html.parser')
		return {
			'number': parsed_volumn_html.find('span', attrs={'class': 'vol-number'}).text,
			'title': parsed_volumn_html.find('span', attrs={'class': 'vol-title'}).text,
        	'cover': parsed_volumn_html.find('img', attrs={'class': 'vol-cover'})['src'],
			'tag': [e.text for e in parsed_volumn_html.find_all('a', attrs={'class': 'vol-tag-item'})],
        	'desc': parsed_volumn_html.find('div', attrs={'class': 'vol-desc'}).text,
			'track': self._parse_track([e.encode('utf8') for e in parsed_volumn_html.find_all('li', attrs={'class': 'track-item'})])
		}

	def _write_volumn_description_file(self, volumn_description):
		if not helper_check_not_exist_mkdir(self._volumn_description_filepath):
			return
		with open(os.path.join(self._volumn_description_filepath, volumn_description['number'] + '.json'), 'w') as fw:
			json.dump(volumn_description, fw, indent=4, ensure_ascii=False)

	def _convert_volumn_description_to_download_info(self, volumn_description):
		download_info = {
			'number': volumn_description['number'],
			'track': []
		}
		for track in volumn_description['track']:
			track_id_pos = track['trackname'].find('.')
			if track_id_pos == -1:
				sys.stderr.write('voldesc2dlinfo err, track[%s]', track)
				continue
			download_info['track'].append(track['trackname'][0:track_id_pos])
		return download_info


class DownloadProcess(Process):
	def __init__(self, baseurl, volumn_download_dir, download_queue):
		super(DownloadProcess, self).__init__()
		self._baseurl = baseurl
		self._volumn_download_dir = volumn_download_dir
		self._download_queue = download_queue

	def run(self):
		while True:
			download_info = self._download_queue.get()
			if download_info is None:
				break

			volumn_number = download_info['number']
			if not helper_check_not_exist_mkdir(os.path.join(self._volumn_download_dir, volumn_number)):
				continue

			for track in download_info['track']:
				mp3_data = requests.get(self._baseurl % (volumn_number, track)).content
				if mp3_data is None:
					sys.stderr.write('download empty data, track[%s]' % track)
					continue
						
				with open(os.path.join(self._volumn_download_dir, download_info['number'], track + '.mp3'), 'wb') as fw:
					fw.write(mp3_data)


def helper_check_not_exist_mkdir(path):
	if os.path.exists(path):
		if os.path.isdir(path):
			return True
		path += '.bak'

	ret = False
	try:
		os.mkdir(path)
		ret = True
	except Exception as e:
		sys.stderr.write('mkdir failed, volno[%s] err[%s]' % (volumn_number, e))
	finally:
		return ret


if __name__ == '__main__':	
	parser = argparse.ArgumentParser(description='luoo.net spider 1.0')
	parser.add_argument('-n', '--number', required=True, nargs='+', help='volumn number list')  
	parser.add_argument('-d', '--dir', default='.\\download', help='volumn dir')
	parser.add_argument('-c', '--concurrency', type=int, default=1, help='concurrency download')
	parser.add_argument('-v', '--volurl', default='http://www.luoo.net/music/', help='volumn url of luoo.net')
	parser.add_argument('-m', '--mp3url', default='http://mp3-cdn.luoo.net/low/luoo/radio%s/%s.mp3', help='mp3 url of luoo.net')
	parser.add_argument('-p', '--proxy', nargs='+', default=[], help='http proxy [ip:port, ip:port]')
	args = parser.parse_args()

	download_queue = Queue()
	crawl_process = CrawlProcess(args.proxy, args.volurl, args.number, args.dir, download_queue)
	crawl_process.start()

	download_process_list = []
	for i in range(args.concurrency):
		download_process = DownloadProcess(args.mp3url, args.dir, download_queue)
		download_process_list.append(download_process)
		download_process.start()

	crawl_process.join()
	for i in range(args.concurrency):
		download_queue.put(None)

	for download_process in download_process_list:
		download_process.join()
