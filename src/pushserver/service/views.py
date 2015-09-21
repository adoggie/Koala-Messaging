__author__ = 'scott'

from django.views.generic import TemplateView,View,FormView
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.http import HttpResponseBadRequest

import forms

class LoginView(View):
	def get(self,request):
		form = forms.LoginForm()
		return render_to_response( 'login.html',context_instance=RequestContext(request,{'form':form}))

	def post(self,request):
		form = forms.LoginForm(data=request.POST)
		if form.is_valid():
			pass
		else:
			print type(form.errors),dir(form.errors)
			return HttpResponseBadRequest( str(form.errors.as_json()) )