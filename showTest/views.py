#coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from .forms import AddForm
from grade_crawle.src import get_crawler
from grade_crawle.src import caluGrade

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