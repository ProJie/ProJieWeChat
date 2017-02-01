# coding=utf-8
from __future__ import unicode_literals


class EventResponse(object) :
	def __init__(self, wechat_obj, message) :
		self.wechat_obj = wechat_obj
		self.message = message
	
	def main(self) :
		"""事件回复的主控制器"""
		response = self.text_response('默认回复')
		if self.message.type == 'subscribe' :  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
			response = self.text_response(text="""感谢您的关注
				接下来你会了解到我是有多么屌!!!""")
		elif self.message.type == 'unsubscribe' :  # 取消关注事件（无可用私有信息）
			response = self.text_response(text='不要取消关注呀~~')
		elif self.message.type == 'scan' :  # 用户已关注时的二维码扫描事件
			response = self.text_response(text='扫描二维码啦~')
		elif self.message.type == 'location' :  # 上报地理位置事件
			response = self.text_response(text='已经收到您自动上报的位置')
		elif self.message.type == 'click' :  # 自定义菜单点击事件
			response = self.customize()
		elif self.message.type == 'view' :  # 自定义菜单跳转链接事件
			response = self.text_response(text='自定义菜单跳转')
		elif self.message.type == 'templatesendjobfinish' :  # 模板消息事件
			response = self.text_response(text='模板消息')
		elif self.message.type in ['scancode_push', 'scancode_waitmsg', 'pic_sysphoto', 'pic_photo_or_album', 'pic_weixin', 'location_select'] :  # 其他事件
			response = self.text_response(text='其他杂七杂八的事件')
		return response
	
	def text_response(self, text) :
		return self.wechat_obj.response_text(content=text)
	
	def customize(self) :
		key = self.message.key
		"""自定义菜单点击事件"""
		if key == 'weather' :
			return self.text_response('想查天气啊...不给你说~~~')
		elif key == 'PHP' :
			return self.text_response('想学PHP啊？？？杰哥带你飞！！！')
		elif key == 'Python' :
			return self.text_response('想学Python？？？这可是个好语言~~~')
		elif key == 'click_good' :
			return self.text_response('感谢点赞,要是能发个红包就更好了O(∩_∩)O~~')
		else :
			return self.text_response('(⊙o⊙)…我的微信公众号出问题了,这个菜单不能用(｡•ˇ‸ˇ•｡)')
