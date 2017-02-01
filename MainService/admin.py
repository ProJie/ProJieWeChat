# coding=utf-8
from __future__ import unicode_literals
from django.contrib import admin

from MainService.models import AutoAnswer


class AutoAnswerAdmin(admin.ModelAdmin) :
	"""自动回复关键词管理"""
	list_display = ['keyword', 'content', 'create_time', 'update_time', 'listable', 'published']


admin.site.register(AutoAnswer, AutoAnswerAdmin)
