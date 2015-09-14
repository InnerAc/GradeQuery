#coding:utf-8
from django import forms

class AddForm(forms.Form):
	RADIO_CHOICES = (
            ('one', "本学期的"),         
            ('all', "全部绩点"),       
    )
	uid = forms.CharField(label='学号',required=False,widget=forms.TextInput(attrs={'placeholder': '学号'}))
	pwd = forms.CharField(label='密码',widget=forms.PasswordInput(attrs={'placeholder': '密码'}))
	check = forms.ChoiceField(widget=forms.RadioSelect, choices=RADIO_CHOICES)