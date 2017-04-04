#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: douban_spider.py
Author: pirdol@qq.com
Date: 2017/04/04 20:35:00
Description: crawl top250 from douban.com
'''

import argparse
import urllib2

from bs4 import BeautifulSoup

class BaseCrawler(object):
	def __init__(self, url):
		self._url = url

	def run(self):
		url = self._url
		while True:
			response = self._crawl(url)
			if response is None or response.getcode() != 200:
				break

			url = self._parse(response.read())
			if url is None:
				break

	def _crawl(self, url):
		try:
			request = urllib2.Request(url, headers={
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
			})
			return urllib2.urlopen(request)
		except Exception as e:
			return None

	def _parse(self, html):
		pass

class BookCrawler(BaseCrawler):
	def __init__(self, url):
		super(BookCrawler, self).__init__(url)
		self._book_list = []

	def _parse(self, html):
		parsed_html = BeautifulSoup(html, 'html.parser')
		for book_html in parsed_html.find_all('tr', attrs={'class': 'item'}):
			title_html = book_html.find('div', attrs={'class': 'pl2'})
			if title_html is None:
				continue
			title_a_html = title_html.find('a')
			title_en_html = title_html.find('span')
			quote_html = book_html.find('span', attrs={'class': 'inq'})
			book = {
				'title': title_a_html.get('title'),
				'url': title_a_html.get('href'),
				'title_en': title_en_html.text if title_en_html else None,
				'publish': book_html.find('p', attrs={'class': 'pl'}).text,
				'rating': book_html.find('span', attrs={'class': 'rating_nums'}).text,
				'comment': book_html.find('span', attrs={'class': 'pl'}).text.replace('\n', '').replace(' ', ''),
				'quote': quote_html.text if quote_html else None
			}
			self._book_list.append(book)

		next_html = parsed_html.find('link', attrs={'rel': 'next'})
		return next_html.get('href') if next_html is not None else None

	def dump(self):
		for index, book in enumerate(self._book_list):
			print index, book.get('title').encode('utf-8')

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='douban.com spider 1.0')
	parser.add_argument('-c', '--channel', required=True, help='book.douban movie.douban ...')
	args = parser.parse_args()

	if args.channel == 'book':
		url = 'http://book.douban.com/top250'
		bc = BookCrawler(url)
		bc.run()
		bc.dump()
	else:
		print 'unknown channel: %s' % args.channel
