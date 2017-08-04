## [Python与简单网络爬虫的编写](http://blog.csdn.net/zhaoyl03/article/details/8631928)

匹配：category、name、magnet、time、size

```python
movie_re = re.compile(r'<tr>.+?\(.+?>(?P<category>.+?)</a>.+?class="detName".+?>(?P<name>.+?)</a></div><a href="(?P<magnet>.+?)".+?<b>(?P<time>.+?)</b>,大小(?P<size>.+?),上传者')
    mo = movie_re.search(html)
    if mo:
        print(mo.group('category'))
        print(mo.group('name'))
        print(mo.group('magnet'))
        print(mo.group('time').replace('&nbsp;', ' '))
        print(mo.group('size').replace('&nbsp;', ' '))
    else:
        print(None)
```

```html
<tr><td class="vertTh"><center><a href="/browse/200"title="此目录中更多">视频</a><br/>(<a href="/browse/205"title="此目录中更多">电视</a>)</center></td><td><div class="detName"><a href="/torrent/7782194/The_Walking_Dead_Season_3_Episodes_1-3_HDTV-x264"class="detLink"title="细节 The Walking Dead Season 3 Episodes 1-3 HDTV-x264">The Walking Dead Season 3 Episodes 1-3 HDTV-x264</a></div><a href="magnet:?xt=urn:btih:4f63d58e51c1a4a997c6f099b2b529bdbba72741&dn=The+Walking+Dead+Season+3+Episodes+1-3+HDTV-x264&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&tr=udp%3A%2F%2Ftracker.istole.it%3A6969&tr=udp%3A%2F%2Ftracker.ccc.de%3A80"title="Download this torrent using magnet"><img src="//static.某piratebay.se/img/icon-magnet.gif"alt="Magnet link"/></a><a href="//torrents.某piratebay.se/7782194/The_Walking_Dead_Season_3_Episodes_1-3_HDTV-x264.7782194.TPB.torrent"title="下载种子"><img src="//static.某piratebay.se/img/dl.gif"class="dl"alt="下载"/></a><img src="//static.某piratebay.se/img/11x11p.png"/><img src="//static.某piratebay.se/img/11x11p.png"/><font class="detDesc">已上传<b>3&nbsp;分钟前</b>,大小2&nbsp;GiB,上传者<a class="detDesc"href="/user/paridha/"title="浏览 paridha">paridha</a></font></td><td align="right">0</td><td align="right">0</td></tr>
```
