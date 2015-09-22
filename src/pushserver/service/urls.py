#coding:utf-8

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings

from rest_framework.routers import  DefaultRouter


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
	url(r'login',views.LoginView.as_view()),
	url(r'register',views.RegisterView.as_view()),
	# url(r'logout'),

)

# urlpatterns += router.urls
# print urlpatterns