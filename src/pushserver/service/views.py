#coding:utf-8

__author__ = 'scott'

from django.views.generic import TemplateView,View,FormView
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.http import HttpResponseBadRequest,HttpResponse

from django.contrib import auth
from django.contrib.auth.models import User as auth_User
import forms

class LoginView(View):
	def get(self,request):
		form = forms.LoginForm()
		return render_to_response( 'login.html',context_instance=RequestContext(request,{'form':form}))

	def post(self,request):
		form = forms.LoginForm(data=request.POST)
		if form.is_valid():
			return HttpResponse('login successful!')
		else:
			print type(form.errors),dir(form.errors)
			errors = {
				'code':100,
				'content':u"用户名或密码错误!"
			}
			return render_to_response( 'login.html',context_instance=RequestContext(request,{'errors':errors,'form':form}))

			# return HttpResponseBadRequest( str(form.errors.as_json()) )

class RegisterView(CreateView):
	model = auth_User
	fields = ('username','password','email')
	# template_name_suffix = '_create_form'
	template_name = 'register.html'
	success_url = 'register_succ.html'

	def form_valid(self, form):
		print form.instance
		return super(RegisterView,self).form_valid(form)

	def form_invalid(self, form):
		print form.errors.as_json()
		print form.instance
		return HttpResponse("wrong data!")
