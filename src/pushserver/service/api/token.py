__author__ = 'zhangbin'


import os,time,datetime,traceback

from desert.misc import genUUID,encodeBase64


def create_device_access_token(**kwargs):
	return encodeBase64( genUUID() )