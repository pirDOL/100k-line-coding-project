#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: test_spider.py
Author: pirdol@qq.com
Date: 2017/03/19 20:35:00
Description: crawl volumn from luoo.net
'''

import unittest
import re
import sys
sys.path.append('.')

from spider import CrawlProcess

class CrawlProcessTestCase(unittest.TestCase):
    def setUp(self):
        self._crawl_process = CrawlProcess([], '', [], '', None)
    
    def tearDown(self):
    	pass

    def testParseTrack(self):
    	track_html = '''<li class="track-item rounded" data-fav="0" id="track17988">
<div class="track-wrapper clearfix">
<span class="btn-control btn-play">
<i class="icon-status-play"></i>
<i class="icon-status-pause"></i>
</span>
<a class="trackname btn-play" href="javascript:;" rel="nofollow">01. Take It Out On Me</a>
<span class="artist btn-play">White Lies</span>
<a class="icon-info" data-sid="17988" data-sname="Take It Out On Me" href="javascript:;" rel="nofollow"></a>
<a class="btn-action-share icon-share" data-app="single" data-id="17988" data-img="http://img-cdn.luoo.net/pics/albums/11466/cover.jpg?imageView2/1/w/580/h/580" data-text="推荐White Lies的歌曲《Take It Out On Me》（分享自@落网）" href="javascript:;" rel="nofollow">
</a>
<a class="btn-action-like icon icon-fav" data-cback="single_like_callback" data-id="17988" data-type="single" href="javascript:;" rel="nofollow">
</a>
</div>
<div class="track-detail-wrapper" id="trackDetailWrapper17988">
<div class="track-detail-arrow">
<img src="http://s.luoo.net/img/trian.png"/>
</div>
<div class="track-detail rounded clearfix">
<div class="player-wrapper">
<img alt="Friends" class="cover rounded" src="http://img-cdn.luoo.net/pics/albums/11466/cover.jpg?imageView2/1/w/580/h/580">
<p class="name">Take It Out On Me</p>
<p class="artist">Artist: White Lies</p>
<p class="album">Album: Friends</p>
</img></div>
<div class="lyric-wrapper">
<div class="lyric-content">
</div>
</div>
</div>
</div>
<!--track-detail-wrapper end-->
</li>'''
    	track_list = self._crawl_process._parse_track([track_html])
    	self.assertEqual(1, len(track_list), track_list)
    	self.assertEqual({'trackname': '01. Take It Out On Me', 'artist': 'White Lies'}, track_list[0])

    def testParseVolumn(self):
    	with open('900.html') as fr:
    		expected = {
    			'number': '900',
				'title': '在这场叫做今天的戏剧中',
        		'cover': 'http://img-cdn.luoo.net/pics/vol/58c6da94e163a.jpg?imageView2/1/w/640/h/452',
				'tag': ['#流行', '#英伦'],
        		'desc': '''
        Take me out tonight
今夜带我出去吧
Where there's music and there's people
那里有音乐和人群
And they're young and alive
那里青春永不息
Driving in your car
坐上你的车
I never never want to go home
我真不想回家
Because I haven't got one
那是因为我
Anymore
一无所有

- The Smiths 

Every breaking wave on the shore
每一个破碎在岸上的浪花
Tells the next one there'll be one more
告知今后还会有更多的前赴后继
And every gambler knows that to lose
每个赌徒都清楚失败
Is what you're really there for
正是你真实的存在过

- U2 

It's not a case
努力使你满足
of aiming to please
那根本不是什么难事
You know you're always crying
但你懂你为什么总是在哭泣
It's just your part
这就是你的角色
In the play
在这场叫做 今天
for today
的戏剧中

- The Cure 

本期音乐为落网第900期音乐期刊，我们又跨过了一个具有象征意义的数字。

在那时，我们在意路上匆忙的人群、在意明媚午后、在意自己是否时髦、以及在意脑海里的所有肆意妄为。在今天，这样一个信息快速且泛滥的时代里，我们再也找不回一整张专辑翻来覆去的听得稀巴烂的状态，只剩下回味里假想的脉脉温情，以及对未来充满着暴力色彩的急切渴求与期盼。在这么多年过去后，我们依然沒有得到自己想要的,可好像這一切也沒有那么糟。

音乐无非就两种，一种是浮在表面的，而另一种则是渗人灵魂的。感谢所有曾经在黑夜中给予我们孤独的灵魂以安抚的声音。

我们明天见。

本期音乐为英伦音乐专题。

Cover From Vincent Bourilhon
''',
				'track': [{'trackname': '01. Take It Out On Me', 'artist': 'White Lies'}, {'trackname': '02. Forget My Name', 'artist': 'One Night Only'}, {'trackname': u"03. Everybody's Changing", 'artist': 'Keane'}, {'trackname': '04. Do No Wrong', 'artist': 'Thirteen Senses'}, {'trackname': '05. For Anyone', 'artist': 'Beady Eye'}, {'trackname': '06. Autumnsong', 'artist': 'Manic Street Preachers'}, {'trackname': '07. Round In Circles', 'artist': 'Hurricane #1'}, {'trackname': '08. Sonnet', 'artist': 'The Verve'}, {'trackname': '09. Lines Of Light', 'artist': 'The Subways'}, {'trackname': '10. Every Breaking Wave', 'artist': 'U2'}, {'trackname': '11. There Is a Light That Never Goes Out', 'artist': 'The Smiths'}, {'trackname': '12. Play For Today', 'artist': 'The Cure'}]
    		}

    		actual = self._crawl_process._parse_volumn(fr.read())
    		self.assertEqual(expected['number'], actual['number'].encode('utf8'))
    		self.assertEqual(expected['title'], actual['title'].encode('utf8'))
    		self.assertEqual(expected['cover'], actual['cover'].encode('utf8'))
    		self.assertEqual(expected['desc'], actual['desc'].encode('utf8'))

    		for i in range(len(expected['tag'])):
    			self.assertEqual(expected['tag'][i], actual['tag'][i].encode('utf8'))
    		
    		for i in range(len(actual['track'])):
    			self.assertEqual(expected['track'][i]['trackname'], actual['track'][i]['trackname'].encode('utf8'))
    			self.assertEqual(expected['track'][i]['artist'], actual['track'][i]['artist'].encode('utf8'))

if __name__ == '__main__':
	unittest.main()
