#coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from .forms import AddForm
from grade_crawle.src import get_crawler
from grade_crawle.src import caluGrade
import random
import json

# Create your views here.

def index(request):
    return HttpResponse(u"Welcome to my world!")
def query(request):
	if request.method == 'POST':
		form = AddForm(request.POST)
		
		if form.is_valid():
			uid = request.POST['uid']
			pwd = request.POST['pwd'] 
			check = request.POST['check']
			subjects = get_crawler.getSource(uid,pwd,check)
			if subjects:
				return render(request,'show.html',{'subjects': subjects})
			else:
				return render(request,'query.html',{'form': form})
	else:
		form = AddForm()
	return render(request,'query.html',{'form': form})
def home(request):
    return render(request, 'home.html')

# for android
def caluKey(types):
	key = 0;
	if types == 1:
		key = random.randint(1, 10000)
		return key
	else:
		return key

def getKey(request,key):
	if key == 'qilin':
		key = caluKey(1)
		response_data = {'key':key}
		return HttpResponse(json.dumps(response_data), content_type="application/json")
def getGrade(request,key,uid,pwd,check):
	if(key == 'qilin'):
		subjects = get_crawler.getSource(uid,pwd,check)
		lists = []
		for subject in subjects:
			if subject != subjects[0]:
				dict = {'subject':subject[0],'grade':subject[1],'score':subject[2]}
				lists.append(dict)
		dicts = {'credit':subjects[0],'subjects':lists}
		return HttpResponse(json.dumps(dicts), content_type="application/json")