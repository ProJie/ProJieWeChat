# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class AutoAnswer(models.Model) :
	"""关键词回复数据表"""
	keyword = models.CharField('关键词', null=False, default='', max_length=256, help_text='用户发送的关键词')
	content = models.CharField('回复内容', null=True, blank=True, max_length=1024, default='', help_text='回复给用户的内容')
	create_time = models.DateTimeField('创建时间', auto_now_add=True)
	update_time = models.DateTimeField('修改时间', auto_now=True, null=False)
	listable = models.BooleanField('是否列出', default=False, help_text='推荐给用户来回复的关键词列表')
	published = models.BooleanField('是否发布', default=True)
	
	def __str__(self) :
		return self.keyword
	
	class Meta :
		verbose_name = '关键词'
		verbose_name_plural = '关键词回复'


@python_2_unicode_compatible
class AccessToken(models.Model) :
	access_token = models.CharField('access_token', max_length=1024, default='')
	access_token_expires_at = models.IntegerField('access_token_expires_at', default=0)
	
	def __str__(self) :
		return self.access_token
