# coding=utf-8
from __future__ import unicode_literals

import time
from vendor.time_handle import *
from django.conf import settings as django_settings


def write_log(filename, data) :
	with open('{}/{}.txt'.format(django_settings.BASE_DIR, filename), 'a+') as f :
		f.write('------------------{}------------------\n'.format(get_real_time(time.time())))
		try :
			f.write(str(data))
		except :
			f.write('写入数据错误!')
		finally :
			f.write('\n------------------{}------------------\n'.format('End'))
