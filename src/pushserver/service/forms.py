#coding:utf-8
__author__ = 'scott'


from django import forms
import model.core.models as core

class LoginForm(forms.Form):
	username = forms.CharField(max_length=20,help_text=u'用户名称',label=u'用户名')
	password = forms.CharField(max_length=20,widget=forms.PasswordInput)

class RegisterForm(forms.Form):
	username = forms.CharField(max_length=20,help_text=u'用户名称')
	password = forms.CharField(max_length=20,widget=forms.PasswordInput)
	email = forms.CharField(max_length=20)


class ApplicationForm(forms.ModelForm):

	class Meta:
		model = core.UserApplication
		fields = ['app_id','app_name','is_active','create_time','access_id','secret_key']

# class ApplicationUpdateForm(forms.ModelForm):
# 	class Meta:
# 		model = core.UserApplication
# 		fields = ['app_id','app_name','is_active','create_time','access_id','secret_key']
