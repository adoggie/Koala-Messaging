#coding:utf-8

from django.conf.urls import patterns, include, url

from api_views import *

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
	url('^push/register/$',RegisterView.as_view(),name='api_register'),
	url('^push/message/$',MessageView.as_view(),name='message'),

]

# urlpatterns += router.urls
# print urlpatterns