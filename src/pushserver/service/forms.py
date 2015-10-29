#coding:utf-8
__author__ = 'scott'


from django import forms
import model.core.models as core

class LoginForm(forms.Form):
	username = forms.CharField(max_length=20,help_text=u'用户名称',label=u'用户名')
	password = forms.CharField(max_length=20,widget=forms.PasswordInput)

class RegisterForm(forms.Form):
	username = forms.CharField(max_length=20,label=u'用户名称',required=False)
	password = forms.CharField(max_length=20,min_length=4,label=u'口令',widget=forms.PasswordInput)
	email = forms.CharField(max_length=20,label=u'账户',widget=forms.EmailInput)




class ApplicationForm(forms.ModelForm):
	create_time = forms.DateTimeField(label=u'创建时间',required=False)
	access_id = forms.CharField(label=u'授权编号',required=False)
	secret_key = forms.CharField(label=u'访问秘钥',required=False)
	class Meta:
		model = core.UserApplication
		fields = ['app_id','app_name','is_active']
		labels ={
			'app_id':u'应用标识',
			'app_name':u'应用名称',
			'is_active':u'启用',
		}
		error_messages ={
			'app_id':{
				'max_length':u'标识不能为空呢！'
			}
		}

# class ApplicationUpdateForm(forms.ModelForm):
# 	class Meta:
# 		model = core.UserApplication
# 		fields = ['app_id','app_name','is_active','create_time','access_id','secret_key']
