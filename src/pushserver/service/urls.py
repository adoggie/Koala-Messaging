#coding:utf-8

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings

from rest_framework.routers import  DefaultRouter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout


# from swarm.app import UserAppViewSet
# from swarm.me import MeViewSet,fetchall
# import service.swarm.me
# import service.swarm.data
# import service.swarm.bizmodel
# import service.hippo.sendmail
# import service.hippo.identify_image
#

import views

domain_pattern = '[a-zA-Z0-9][-a-zA-Z0-9]{0,62}'
urlpatterns = patterns('',
	url(r'^api/$',include('service.api.urls')),
	url(r'login',views.LoginView.as_view(),name='login'),
	url(r'logout',logout,{'next_page':'login'}),
	url(r'register/$',views.RegisterView.as_view()),
	url(r'main/$', login_required( views.MainView.as_view()) ),
	url(r'register_succ/$',TemplateView.as_view(template_name="register_succ.html"))

	# url(r'logout'),

)

# urlpatterns += router.urls
# print urlpatterns