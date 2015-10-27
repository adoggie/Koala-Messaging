#coding:utf-8

__author__ = 'scott'

from django.views.generic import TemplateView,View,FormView
from django.views.generic.list import  ListView

from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.shortcuts import render_to_response,render,redirect
from django.template import RequestContext
from django.http import HttpResponseBadRequest,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User as auth_user,UserManager

from model.core.models import PushUserAccount
import model.core.models as core



from django.contrib import auth
# from django.contrib.auth.models import User as auth_User
import forms

class LoginView(View):
	def get(self,request):
		form = forms.LoginForm()

		return render_to_response( 'login.html',context_instance=RequestContext(request,{'form':form}))

	def post(self,request):
		form = forms.LoginForm(data=request.POST)
		errors = {}
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username,password=password)
			if user:
				login(request,user)
				return redirect('/main')
			else:
				errors = {
				'code':100,
				'content':u"you wrong!"
				}
				return render_to_response('login.html',context_instance=RequestContext(request,{'form':form,'errors':errors}))

		else:
			print type(form.errors),dir(form.errors)
			errors = {
				'code':100,
				'content':u"用户名或密码错误!"
			}
			return render_to_response( 'login.html',context_instance=RequestContext(request,{'errors':errors,'form':form}))

			# return HttpResponseBadRequest( str(form.errors.as_json()) )

class RegisterView(FormView):
	# model = auth_user
	# fields = ('username','password','email')
	# template_name_suffix = '_create_form'
	form_class = forms.RegisterForm
	template_name = 'register.html'
	success_url = 'register_succ'

	def form_valid(self, form):
		errors=[]
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		email = form.cleaned_data['email']
		user = auth_user.objects.create_user(username,email,password)
		acct = PushUserAccount(user = user)
		acct.save()
		return super(RegisterView,self).form_valid(form)

	def form_invalid(self, form):
		print form.errors.as_json()
		print form.instance
		return HttpResponse("wrong data!")


# class MainView(TemplateView):
class MainView(ListView):
	template_name = "main.html"
	paginate_by = 5

	def get_context_data(self, **kwargs):
		ctx = super(MainView,self).get_context_data(**kwargs)
		return ctx

	def get_queryset(self):
		rs = self.request.user.auth_user.user_apps.all()
		return rs


class ApplicationListView(ListView):
	template_name = "main.html"
	paginate_by = 5

	def get_context_data(self, **kwargs):
		ctx = super(MainView,self).get_context_data(**kwargs)
		return ctx

	def get_queryset(self):
		rs = self.request.user.auth_user.user_apps.all()
		return rs

class ApplicationDeleteView(DeleteView):
	model = core.UserApplication
	success_url = '/main'

	def delete(self, request, *args, **kwargs):
		# obj = self.get_object()
		# obj.app_devices.all().delete()
		super(ApplicationDeleteView,self).delete(request,*args,**kwargs)
