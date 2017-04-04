#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: weibo_cn_login.py
Author: pirdol@qq.com
Date: 2017/04/04 15:15:00
Description: login weibo.cn
'''

import argparse

import requests
from bs4 import BeautifulSoup

class WeiboCnLogin(object):
	def __init__(self, url, username, passwd, cookie_filepath):
		self._url = url
		self._username = username
		self._passwd = passwd
		self._cookie_filepath = cookie_filepath

	def login(self):
		response = self._login_by_cookie()
		if response is None:
			pass
			return

		parsed_weibo = self._parse_html(response.content)
		print parsed_weibo, response.content
		for nickname, content in zip(parsed_weibo.get('nk', []), parsed_weibo.get('ctt', [])):
			print '%s %s' % (nickname, content)

	def _parse_html(self, html):
		parsed_html = BeautifulSoup(html, 'html.parser')
		return {
			'nk': [e.text.encode('utf-8') for e in parsed_html.find_all('a', attrs={'class': 'nk'})],
			'ctt': [e.text.encode('utf-8') for e in parsed_html.find_all('span', attrs={'class': 'ctt'})]
		}

	def _login_by_cookie(self):
		cookie = self._get_cookie_from_file(self._cookie_filepath)
		if cookie == '':
			return None
		return requests.get(self._url, headers={
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0',
   			'Cookie': cookie
		})

	def _login_by_passwd(self):
		pass

	def _get_cookie_from_file(self, cookie_filepath):
		try:
			with open(cookie_filepath) as fr:
				return fr.read()
		except Exception as e:
			return ''

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='weibo.cn login 1.0')
	parser.add_argument('-u', '--username', help='username')  
	parser.add_argument('-p', '--passwd', help='password')
	parser.add_argument('-c', '--cookie', default='', help='/path/to/cookie')
	parser.add_argument('-H', '--host', default='http://weibo.cn', help='login url')
	args = parser.parse_args()

	wl = WeiboCnLogin(args.host, args.username, args.passwd, args.cookie)
	wl.login()
