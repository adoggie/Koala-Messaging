#coding:utf-8

from django.conf.urls import patterns, include, url

from api_views import *

from rest_framework.routers import  DefaultRouter

# import service
# import service.swarm.app.UserAppViewSet

# router = DefaultRouter()
#
#
# router.register(r'WEBAPI/appserver/app-account',UserAppViewSet,'account')	#第三方账号绑定
#
# router.register(r'WEBAPI/appserver/data/analyses', service.swarm.data.DataAnalysesViewSet,'data')	#第三方账号绑定
# router.register(r'WEBAPI/appserver/bizmodels', service.swarm.bizmodel.BizModelViewSet,'bizmodel')	#模型视图

domain_pattern = '[a-zA-Z0-9][-a-zA-Z0-9]{0,62}'
urlpatterns = patterns('',
	url('push/register/$',RegisterView.as_view(),'register'),

	# url(r'^WEBAPI/appserver/domain/(%s)/$'%domain_pattern,'service.swarm.domain.domain_probe',name='test1'),
	# url(r'^WEBAPI/auth/accessToken/$',service.auth.token.user_login,name='userlogin'),
	# url(r'^WEBAPI/auth/accessToken/detail/$',service.auth.token.decode_user_token,name='token_detail'),
	# url(r'^WEBAPI/auth/restricted/orguser/login/$',service.auth.restricted.orguser_login,name='orguser_login'),


)

urlpatterns += router.urls
print urlpatterns