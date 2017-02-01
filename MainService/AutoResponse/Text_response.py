# coding=utf-8
from __future__ import unicode_literals

import json
import requests
from MainService.models import AutoAnswer


class TextResponse(object) :
	def __init__(self, wechat_obj, message) :
		self.wechat_obj = wechat_obj
		self.message = message
	
	def main(self) :
		content = self.message.content
		response = self.text_response(content)
		try :
			keyword_db = AutoAnswer.objects.get(keyword=content, published=True)
		except AutoAnswer.DoesNotExist :
			keyword_db = False
		if content.endswith('天气') :
			response = self.weather(content.split('天气')[0])
		elif keyword_db :
			response = self.text_response(keyword_db.content)
		
		return response
	
	def weather(self, location) :
		if location == '' or not location :
			return self.text_response('您需要输入地理位置,比如：焦作天气')
		"""天气查询接口"""
		url = 'http://wthrcdn.etouch.cn/weather_mini'
		res = requests.get(url=url, params={'city' : location})
		try :
			date = json.loads(res.content)['data']
		except KeyError :
			return self.text_response('找不到{}的天气'.format(location))
		text = """当前气温：{}摄氏度
		感冒指数：{}
		{}""".format(
				date['wendu'],
				date['ganmao'],
				''.join([
					        '''----~{}~----
							天气：{}
							最高温度：{}
							最低温度：{}
							风力：{}{}
							'''.format(w['date'], w['type'], w['high'], w['low'], w['fengxiang'], w['fengli'])
					        for w in date['forecast']
					        ])
		)
		return self.text_response(text)
	
	def text_response(self, text) :
		return self.wechat_obj.response_text(content=text)
