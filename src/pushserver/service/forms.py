#coding:utf-8
__author__ = 'scott'


from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(max_length=20,help_text=u'用户名称')
	password = forms.CharField(max_length=20,widget=forms.PasswordInput)
