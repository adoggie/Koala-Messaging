__author__ = 'zhangbin'


class CacheEntryFormat:
	UserWithTGS = 'user_tgs:%s'

class PlatformType:
	P_UNDEFINED = 0
	P_ANDROID = 1
	P_IOS = 2
	P_DESKTOP = 4
	P_HTML5 = 8


class MessageConfirmValue:
	UNACKED = 0
	ACKED = 1
