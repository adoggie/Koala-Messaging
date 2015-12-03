#coding:utf-8

__author__ = 'scott'

import datetime,traceback,sys,os,time

from django.views.generic import TemplateView,View,FormView,DetailView
from django.views.generic.list import  ListView
from django.shortcuts import render_to_response

from django.views.generic.edit import CreateView,DeleteView,UpdateView,\
	ModelFormMixin,FormMixin,DeletionMixin
from django.shortcuts import render_to_response,render,redirect
from django.template import RequestContext
from django.http import HttpResponseBadRequest,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User as auth_user,UserManager
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from desert.misc import genUUID,random_password

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
	success_url = '/main/'

	def form_valid(self, form):
		errors=[]
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		email = form.cleaned_data['email']
		username = email
		if auth_user.objects.filter( username = username).count():
			form._errors = "User Name:%s has existed!"%username
			return   super(RegisterView,self).form_invalid(form)

		user = auth_user.objects.create_user(username,email,password)
		acct = PushUserAccount(user = user)
		acct.save()

		user = authenticate(username=username,password=password)
		if user:
			login(self.request,user)
		return super(RegisterView,self).form_valid(form)

	def form_invalid(self, form):
		# print form.errors.as_json()
		# print form.instance
		return super(RegisterView,self).form_invalid(form)

		# return HttpResponse("wrong data!")

class ApplicationCreateView(CreateView):
	form_class = forms.ApplicationForm
	template_name = "app_detail.html"
	success_url = '/main'

	def get(self, request, *args, **kwargs):
		form = forms.ApplicationForm(initial={"is_active":True,'app_id':'x.y.z','app_name':'your app name'})
		return render_to_response( 'app_detail.html',context_instance=RequestContext(request,{'form':form}))


	def form_valid(self, form):
		form.instance.create_time = datetime.datetime.now()
		form.instance.access_id = genUUID()
		form.instance.secret_key = random_password()
		form.instance.account = self.request.user.auth_user
		return super(ApplicationCreateView,self).form_valid(form)


	def form_invalid(self, form):
		errors = form.errors

		return render_to_response( 'app_detail.html',context_instance=RequestContext(self.request,{'form':form,'errors':errors}))

# class ApplicationUpdateView(UpdateView):
# 	# form_class =  forms.ApplicationForm
# 	model = core.UserApplication
# 	fields = ['app_name','is_active']
# 	template_name = "app_detail.html"
# 	success_url = '/main'
#
# 	def get(self, request, *args, **kwargs):
# 		super(ApplicationUpdateView,self).get(self,request,*args,**kwargs)
#
# 	def form_valid(self, form):
#
# 		return super(ApplicationUpdateView,self).form_valid(form)
#
# 	def form_invalid(self, form):
# 		errors = form.errors
# 		return redirect()
# 		return render_to_response( 'app_detail.html',context_instance=RequestContext(self.request,{'form':form,'errors':errors}))


class ApplicationDetailView( ModelFormMixin, DetailView):
	# form_class =  forms.ApplicationForm
	# def get(self, request, *args, **kwargs):
	model = core.UserApplication
	template_name = "app_detail.html"
	fields = ['app_name','is_active']
	success_url = '/main'
	paginate_by = 5

	def get_context_data(self,**kwargs):
		ctx = super(ApplicationDetailView,self).get_context_data(**kwargs)
		ctx['form'] = forms.ApplicationForm(instance= ctx['object'])
		return ctx

	def post(self,request,*args,**kwargs):
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):

		return super(ApplicationDetailView,self).form_valid(form)

	def form_invalid(self, form):
		errors = form.errors
		# return redirect()
		return super(ApplicationDetailView,self).form_invalid(form)

class ApplicationUpdatelView( UpdateView ):
	model = core.UserApplication
	template_name = "app_detail.html"
	fields = ['app_name','is_active','address_restricted']
	success_url = '/applications/'
	paginate_by = 5

	def get_context_data(self,**kwargs):
		ctx = super(ApplicationUpdatelView,self).get_context_data(**kwargs)
		if not ctx['form'].data:
			ctx['form'].data = ctx['object']
		# ctx['form'] = forms.ApplicationForm(instance= ctx['object'])
		return ctx



class ApplicationDeviceListView(ListView):
	paginate_by = 2
	template_name = "dev_list.html"

	def get(self, request, *args, **kwargs):
		return super(ApplicationDeviceListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		pk = self.kwargs.get('pk')
		self.app = core.UserApplication.objects.get(id = pk)
		rs = self.app.app_devices.all()
		return rs

	def get_context_data(self, **kwargs):
		ctx = super(ApplicationDeviceListView,self).get_context_data(**kwargs)
		ctx['app'] = self.app
		return ctx


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


class RestrictedAddressListView(ListView):
	paginate_by = 2
	template_name = "address_restricted_list.html"


	def get_queryset(self):
		pk = self.kwargs.get('pk')
		self.app = core.UserApplication.objects.get(id = pk)
		rs = self.app.address_restricted_set.all().order_by('name')
		return rs

	def get_context_data(self, **kwargs):
		ctx = super(RestrictedAddressListView,self).get_context_data(**kwargs)
		ctx['app'] = self.app
		return ctx


class RestrictedAddressCreateView(CreateView):
	# form_class = forms.ApplicationForm
	model = core.PushAddressRestricted
	fields = ['name','address','mask','is_black','is_active']
	template_name = "address_restricted_detail.html"
	success_url = '/main'

	def get(self, request, *args, **kwargs):
		pk = self.kwargs.get('pk')
		self.app = core.UserApplication.objects.get(id = pk)

		return super(RestrictedAddressCreateView,self).get(self,request,*args,**kwargs)

		# form = forms.ApplicationForm(initial={"is_active":True,'app_id':'x.y.z','app_name':'your app name'})
		# return render_to_response( 'app_detail.html',context_instance=RequestContext(request,{'form':form}))

	def post(self, request, *args, **kwargs):
		pk = self.kwargs.get('pk')
		self.app = core.UserApplication.objects.get(id = pk)
		return super(RestrictedAddressCreateView,self).post(self,request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		ctx = super(RestrictedAddressCreateView,self).get_context_data(**kwargs)
		ctx['app'] = self.app
		return ctx

	def form_valid(self, form):
		# form.instance.create_time = datetime.datetime.now()
		# form.instance.access_id = genUUID()
		# form.instance.secret_key = random_password()
		# form.instance.account = self.request.user.auth_user
		form.instance.app = self.app
		form.instance.comment = self.request.POST.get('comment')
		return super(RestrictedAddressCreateView,self).form_valid(form)


	def form_invalid(self, form):
		errors = form.errors
		return super(RestrictedAddressCreateView,self).form_invalid(form)
		# return render_to_response( 'app_detail.html',context_instance=RequestContext(self.request,{'form':form,'errors':errors}))

	def get_success_url(self):
		self.success_url = reverse('app-address-restricted',args=[self.object.app.id])
		return self.success_url


class RestrictedAddressUpdatelView( UpdateView ):
	model = core.PushAddressRestricted
	fields = ['name','address','mask','is_black','is_active']
	template_name = "address_restricted_detail.html"
	success_url = '/main'

	def get_context_data(self,**kwargs):
		ctx = super(RestrictedAddressUpdatelView,self).get_context_data(**kwargs)
		if not ctx['form'].data:
			ctx['form'].data = ctx['object']
		return ctx

	def get(self, request, *args, **kwargs):
		pk = self.kwargs.get('pk_app')
		self.app = core.UserApplication.objects.get(id = pk)

		return super(RestrictedAddressUpdatelView,self).get(self,request,*args,**kwargs)

	def post(self, request, *args, **kwargs):
		pk = self.kwargs.get('pk_app')
		self.app = core.UserApplication.objects.get(id = pk)
		return super(RestrictedAddressUpdatelView,self).post(self,request,*args,**kwargs)

	def form_valid(self, form):
		form.instance.app = self.app
		form.instance.comment = self.request.POST.get('comment')
		return super(RestrictedAddressUpdatelView,self).form_valid(form)

	def get_success_url(self):
		self.success_url = reverse('app-address-restricted',args=[self.object.app.id])
		return self.success_url


class RestrictedAddressDeleteView(DeleteView):
	model = core.PushAddressRestricted
	# success_url = reverse('app-address-restricted')

	# def get_context_data(self,**kwargs):
	# 	ctx = super(RestrictedAddressUpdatelView,self).get_context_data(**kwargs)
	# 	if not ctx['form'].data:
	# 		ctx['form'].data = ctx['object']
	# 	return ctx
	#
	# def get(self, request, *args, **kwargs):
	# 	pk = self.kwargs.get('pk_app')
	# 	self.app = core.UserApplication.objects.get(id = pk)
	#
	# 	return super(RestrictedAddressUpdatelView,self).get(self,request,*args,**kwargs)

	#
	def get_success_url(self):
		self.success_url = reverse('app-address-restricted',args=[self.object.app.id])
		return self.success_url

class MessagingView(View):
	def get(self,request):
		apps = request.user.auth_user.user_apps.all()
		context={'apps':apps,'view':self}
		return render_to_response('messaging.html',context_instance=RequestContext(self.request,context))