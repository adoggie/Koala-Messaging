#coding:utf-8

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView,DeleteView,DetailView,CreateView,RedirectView
from django.conf import settings

# from rest_framework.routers import  DefaultRouter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
import model.core.models as core


from . import views

domain_pattern = '[a-zA-Z0-9][-a-zA-Z0-9]{0,62}'

urlpatterns = patterns('',
	url(r'^api/',include( 'service.api.urls' )),
	url(r'^login/$',views.LoginView.as_view(),name='login'),
	url(r'^logout/$',logout,{'next_page':'login'},name='logout'),
	url(r'^register/$',views.RegisterView.as_view(),name='register'),
	url(r'^main/$',  login_required( views.MainView.as_view() ),name='main' ),
	url(r'^register_succ/$',TemplateView.as_view(template_name="register_succ.html")),


	url(r'^applications/$',RedirectView.as_view(url='/main',permanent=True),name='app-list'),
	url(r'^applications/(?P<pk>[0-9]+)/delete/$',login_required(DeleteView.as_view(
		model=core.UserApplication,success_url='/applications'),
	),name='app-delete'),

	url(r'^applications/(?P<pk>[0-9]+)/$',login_required( views.ApplicationDetailView.as_view() ),name='app-detail'),
	url(r'^applications/new/$',login_required( views.ApplicationCreateView.as_view()),name='app-create'),
	url(r'^applications/(?P<pk>[0-9]+)/devices/$',login_required( views.ApplicationDeviceListView.as_view() ),name='app-device-list'),
	url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),

)

# urlpatterns += router.urls
# print urlpatterns