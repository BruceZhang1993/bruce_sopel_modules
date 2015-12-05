#!/usr/bin/python
## -*- coding: utf-8 -*-
from sopel import module
import requests
import json

@module.commands("bilibili")
def bili(bot, trigger):
	arg = trigger.group(2)
	for item in get_msgs(arg):
		bot.reply(item)

def get_video(mid):
	r = requests.get('http://space.bilibili.com/ajax/member/getSubmitVideos?mid=%s&pagesize=3&tid=0&keyword=&page=1'%(mid))
	j = json.loads(r.content.decode())
	if j['status']:
		return j['data']['vlist']
	else:
		return False

def get_msgs(mid):
	result = get_video(mid)
	msgs = ["%s  的最新视频："%(result[0]['author']) ]
	for item in result:
		url = "http://www.bilibili.com/video/av%s/"%(item['aid'])
		msgs.append("[ %s ] -- URL: %s"%(item['title'], url))
	return msgs
