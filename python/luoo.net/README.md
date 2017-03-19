#### [爬虫学习之一个简单的网络爬虫](http://python.jobbole.com/85653/)

时间：20170319 20:35-23:35

内容：从[落网](luoo.net)爬取某个专辑的歌曲内容，并下载到本地

踩坑：

1. `json.dump`如果有中文，默认是转义成ascii码表示的`\uXXXX`的，显式指定`ensure_ascii=False`才能把中文编码为utf8写入文件
2. `BeautifulSoup.find`返回的字符串是unicode的str
3. `BeautifulSoup(html, 'html.parser')`如果html已经是unicode了（例如把`BeautifulSoup.find`的返回值作为html参数），那么后续find就会失败，需要`html.encode('utf8')`