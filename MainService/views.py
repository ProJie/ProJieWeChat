# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
# Django
import json

import time
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from MainService.models import AccessToken
# WechatSDK
from wechat_sdk import WechatBasic, WechatConf
from wechat_sdk.messages import *
# AutoResponse
from AutoResponse.Event_resopnse import EventResponse
from MainService.AutoResponse.Text_response import TextResponse


def get_new_access_token() :
	"""根据时间戳来判断数据库是否有未过期的access_token"""
	timestamps = int(time.time())
	access_token_records = AccessToken.objects.filter(access_token_expires_at__gt=timestamps - 7200)
	if len(access_token_records) == 0 :
		wechat_obj = WechatBasic(
				token='projie',
				appid='wxe1c1f049439b6c30',
				appsecret='f85b53570ae1540b078e548b99a45f6c',
		)
		new_access_token = wechat_obj.get_access_token()
		AccessToken.objects.create(access_token=new_access_token['access_token'], access_token_expires_at=new_access_token['access_token_expires_at'])
		return new_access_token['access_token'], new_access_token['access_token_expires_at']
	else :
		return access_token_records[0].access_token, access_token_records[0].access_token_expires_at


@csrf_exempt
def index(request) :
	"""微信公众号的主控制器"""
	access_token, access_token_expires_at = get_new_access_token()
	wechat_obj = WechatBasic(
			token='projie',
			appid='wxe6dd92b5d69334ad',
			appsecret='6f377e6996fed8734832531b9503e9f3',
			access_token=access_token,
			access_token_expires_at=int(access_token_expires_at)
	
	)
	if request.method == 'GET' :  # 执行token验证
		if wechat_obj.check_signature(
				signature=request.GET.get('signature'),
				timestamp=request.GET.get('timestamp'),
				nonce=request.GET.get('nonce')
		) :
			return HttpResponse(request.GET.get('echostr'), content_type="text/plain")
		else :
			return HttpResponseBadRequest('Verify Error')
	else :  # 各种回复消息
		
		try :
			wechat_obj.parse_data(request.body)
		except ParseError :
			return HttpResponseBadRequest('XML PARSE ERROR')
		# 获取消息的主体内容
		message = wechat_obj.get_message()
		# 默认的回复内容
		response = wechat_obj.response_text(content="你好,欢迎关注我的微信公众号!")
		if isinstance(message, TextMessage) :  # 文本消息
			Txt = TextResponse(wechat_obj, message)
			response = Txt.main()
		elif isinstance(message, ImageMessage) :  # 图片消息
			response = wechat_obj.response_text(content='这是什么图')
		elif isinstance(message, VoiceMessage) :  # 语音消息
			response = wechat_obj.response_text(content=message.recognition)
		elif isinstance(message, VideoMessage) or isinstance(message, ShortVideoMessage) :  # 视频消息
			response = wechat_obj.response_text(content='天天就知道看片')
		elif isinstance(message, LocationMessage) :  # 位置信息
			response = wechat_obj.response_text(content='你在这里呀')
		elif isinstance(message, LinkMessage) :  # 链接消息
			response = wechat_obj.response_text(content='这是**网站?')
		elif isinstance(message, EventMessage) :  # 事件
			event = EventResponse(wechat_obj, message)
			response = event.main()
		
		# 执行回复
		return HttpResponse(response, content_type="application/xml")
