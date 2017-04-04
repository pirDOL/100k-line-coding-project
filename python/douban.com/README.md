## [Python 爬虫-模拟登录知乎-爬取拉勾网职位信息](http://python.jobbole.com/85511/)

时间：20170404 20:35-23:35

内容：从豆瓣读书爬取top250的书籍信息

笔记：
1. `BeautifulSoup.find()`失败返回None，如果不检查，直接调用`.text`、`.get()`会抛异常
2. `BeautifulSoup.find`和`BeautifulSoup.get()`的区别，以获取书籍标题为例：
```python
title_html = book_html.find('div', attrs={'class': 'pl2'})
title_a_html = title_html.find('a') # 从html中查找tag
title = title_a_html.text           # 获取tag的文本
url = title_a_html.get('href')        # 获取tag的属性
```

```html
<div class="pl2">
    <a href="https://book.douban.com/subject/1770782/" onclick="&quot;moreurl(this,{i:'0'})&quot;" title="追风筝的人">
                追风筝的人

                
              </a>



                &nbsp; <img src="https://img3.doubanio.com/pics/read.gif" alt="可试读" title="可试读">

              
    <br>
    <span style="font-size:12px;">The Kite Runner</span>
</div>
```
