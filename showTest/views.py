#coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from .forms import AddForm
# Create your views here.

def index(request):
    return HttpResponse(u"Welcome to my world!")
def add1(request,a,b):
	c = int(a) + int(b)
	return HttpResponse(str(c))
	
def query(request):
	if request.method == 'POST':
		form = AddForm(request.POST)
		
		if form.is_valid():
			uid = request.POST['uid']
			pwd = request.POST['pwd'] 
			c = uid + pwd
			return HttpResponse(c)
	else:
		form = AddForm()
	return render(request,'query.html',{'form': form})
def home(request):
    return render(request, 'home.html')