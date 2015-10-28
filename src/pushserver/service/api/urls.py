#coding:utf-8

from django.conf.urls import patterns, include, url

# from api_views import *

import api_views

# from rest_framework.routers import  DefaultRouter

# import service
# import service.swarm.app.UserAppViewSet

# router = DefaultRouter()
# router.register(r'WEBAPI/appserver/app-account',UserAppViewSet,'account')	#第三方账号绑定
#
# router.register(r'WEBAPI/appserver/data/analyses', service.swarm.data.DataAnalysesViewSet,'data')	#第三方账号绑定
# router.register(r'WEBAPI/appserver/bizmodels', service.swarm.bizmodel.BizModelViewSet,'bizmodel')	#模型视图

domain_pattern = '[a-zA-Z0-9][-a-zA-Z0-9]{0,62}'
urlpatterns = [
	url('^push/register/$',api_views.RegisterView.as_view(),name='api_register'),
	# url('^push/message/$',api_views.MessageView.as_view(),name='message'),
	url('^push/simple/all/$',api_views.simple_all,name='push-simple-all'),
	url('^push/simple/device/$',api_views.simple_device,name='push-simple-device'),
	url('^push/simple/account/$',api_views.simple_account,name='push-simple-account'),
	url('^push/simple/tag/$',api_views.simple_tag,name='push-simple-tag'),


]

# urlpatterns += router.urls
# print urlpatterns