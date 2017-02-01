# coding=utf-8
import time


def get_timestamp(old_time) :
	"""从y-m-d获取时间戳"""
	time_list = time.strptime(old_time, '%Y-%m-%d')
	timestamp = time.mktime(time_list)
	return timestamp


def get_real_time(timestamp, l=6) :
	"""从时间戳获取到时间ymdhms"""
	ltime = time.localtime(int(float(timestamp)))
	if l == 3 :
		real_time = time.strftime('%Y-%m-%d', ltime)
	elif l == 6 :
		real_time = time.strftime('%Y-%m-%d %H:%M:%S', ltime)
	else :
		real_time = time.strftime('%Y-%m-%d %H:%M:%S', ltime)
	return real_time
