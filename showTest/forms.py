#coding:utf-8
from django import forms

class AddForm(forms.Form):
	uid = forms.CharField(label='学号',required=False)
	pwd = forms.CharField(label='密码',widget=forms.PasswordInput)