#!/usr/bin/python
## -*- coding: utf-8 -*-
from sopel import module
import requests
import json
import random
import datetime
import re

command = ["express", "kd"]
@module.commands(*command)
def kuaidi(bot, trigger):
	keywords = trigger.group(2)
	arglist = re.split('\s+', keywords)
	if len(arglist) > 2:
		bot.reply(get_error(2))
	elif len(arglist) == 0:
		bot.reply(get_error(3))
	elif len(arglist) == 1 and arglist[0] == 'help':
		bot.reply(get_error(3))
	elif len(arglist) == 1 and arglist[0].isdigit():
		results = quick_check(arglist[0])
		lines = 5
		for result in results:
			if lines == 0:
				break
			bot.msg(trigger.user, result)
			lines -= 1
		bot.msg(trigger.sender, "查询结果以私信发送，请查看。")
	elif not arglist[0].isdigit():
		bot.reply(get_error(4))
	elif len(arglist) == 2:
		results = get_status(arglist[0], arglist[1])
		lines = 5
		for result in results:
			if lines == 0:
				break
			bot.msg(trigger.user, result)
			lines -= 1
		bot.msg(trigger.sender, "查询结果以私信发送，请查看。")

def get_com(eid):
	comlist = []
	url = "http://www.kuaidi100.com/autonumber/autoComNum?text=" + str(eid)
	response = requests.post(url)
	resdict = json.loads(response.content.decode())
	coms = resdict['auto']
	for com in coms:
		comlist.append(com['comCode'])
	return comlist

def get_status(eid, com):
	msgs = []
	query = '?type='+com+'&postid='+str(eid)+'&valicode=&temp='+str(random.random())
	url = 'http://www.kuaidi100.com/query'
	req = requests.get(url+query)
	edict = json.loads(req.content.decode())
	if edict['message'] != 'ok':
		return 1
	else:
		msgs.append("快递单号："+str(eid)+" 快递公司代号："+com+" 当前状态"+is_check(edict))
		for item in edict['data']:
			msg = item['context'] + ' --- ' + time_till_now(item['time'])
			msgs.append(msg)
		return msgs

def time_till_now(timestr):
	timenum = []
	timelist = re.split(':| |-', timestr)
	for num in timelist:
		timenum.append(int(num))
	now = datetime.datetime.now()
	then = datetime.datetime(*timenum)
	if (now-then).days > 0:
		return "%d天前"%(now-then).days
	elif (now-then).seconds >= 3600:
		return str((now-then).seconds / 3600) + '小时前'
	else: return str((now-then).seconds / 60) + '分钟前'

def is_check(dict):
	if dict['ischeck'] == '1':
		return '已签收'
	else:
		return '待签收'

def quick_check(eid):
	comlist = get_com(eid)
	if len(comlist) == 0:
		return 0
	else:
		com = comlist[0]
		return get_status(eid, com)

def get_error(errno):
	return errors[errno]

errors = [
	"无法自动检测快递公司，尝试命令： express/kd [快递单号] [快递公司拼音全称]。",
	"无法找到此快递单号对应的信息，单号输入有误或状态信息有延迟。",
	"参数过多，命令格式： express/kd [快递单号] <[快递公司拼音全称]>(可选项)。",
	"命令格式： express/kd [快递单号] <[快递公司拼音全称]>(可选项)。",
	"快递单号输入有误，可能包含非数字字符。"
]
