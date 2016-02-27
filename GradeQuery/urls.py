"""GradeQuery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from GradeQuery import settings
from django.conf import settings
# from django.conf.urls.static import static
import GradeQuery

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # only test
    url(r'^query$','showTest.views.query',name='query'),
    url(r'^$', 'showTest.views.query', name='home'),
    url(r'^show/([a-z A-Z \d]+)$','showTest.views.show',name='show'),
    # for android
    url(r'^qilin/getkey/([a-z A-Z \d]+)$','showTest.views.getKey', name='getkey'),
    url(r'^qilin/getgrade/([a-z A-Z \d]+)/([a-z A-Z \d]+)/([a-z A-Z \d]+)/([a-z A-Z \d]+)$','showTest.views.getGrade', name='getgrade'),
]
