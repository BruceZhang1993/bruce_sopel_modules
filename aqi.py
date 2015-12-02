#!/usr/bin/python
## -*- coding: utf-8 -*-
from sopel import module
import json
import requests
from pprint import pprint

# 这里输入申请的 APIKey， 申请地址：http://pm25.in/api_doc
token = "5j1znBVAsnSf5xQyNQyq"

command = ["aqi", "kq"]
@module.commands(*command)
def dice(bot, trigger):
	query = trigger.group(2)
	if query == "":
		bot.reply("AQI(空气质量指数)查询命令格式： $aqi/kq [查询城市] 。")
	else:
		for msg in get_formatted_aqi(query):
			bot.reply(msg)

rank_comm = ["aqi.rank", "kq.rank"]
@module.commands(*rank_comm)
def rank(bot, trigger):
	for msg in get_rank():
		bot.reply(msg)

def get_rank():
	msgs = []
	url = "http://www.pm25.in/api/querys/aqi_ranking.json?token=%s"%(token)
	response = requests.get(url)
	result = json.loads(response.content.decode())
	if type(result) == dict:
		msgs.append(result['error'])
	else:
		msg = "空气质量最佳城市TOP5: "
		for i in range(0, 5):
			msg += "[%d] %s 空气污染指数： %d, %s。 "%(i+1, result[i]['area'], result[i]['aqi'], result[i]['quality'])
		msgs.append(msg)
		msg = "空气质量最差城市TOP5: "
		for i in range(0, 5):
			msg += "[%d] %s 空气污染指数： %d, %s。 "%(i+1, result[len(result)-1-i]['area'], result[len(result)-1-i]['aqi'], result[len(result)-1-i]['quality'])
		msgs.append(msg)
	return msgs

def get_aqi(city):
	url = "http://www.pm25.in/api/querys/aqi_details.json?token=%s&city=%s&stations=no&avg=true"%(token, city)
	response = requests.get(url)
	result = json.loads(response.content.decode())
	return result

def get_formatted_aqi(city):
	result = get_aqi(city)
	if type(result) == dict:
		msgs = [ result['error'] ]
	else:
		c = result[0]['area']
		aqi = result[0]['aqi']
		pri = result[0]['primary_pollutant']
		pm25 = result[0]['pm2_5']
		pm10 = result[0]['pm10']
		quality = result[0]['quality']
		if pri == "":
			pri = "无"
		msgs = [
			"%s AQI(空气质量指数) 查询结果： "%(c),
			"空气污染指数： %d， 空气质量： %s， 首要污染物： %s， 实时PM2.5: %d， 实时PM10: %d  "%(aqi, quality, pri, pm25, pm10)
		]
	return msgs

pprint(get_rank())