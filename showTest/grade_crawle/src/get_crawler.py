# -*- coding: utf-8 -*-
import sys 
import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import cookielib  
import string  
import re  
from segmentation import NormalSegmenter
from feature_extraction import SimpleFeatureExtractor
from analyzer import KNNAnalyzer
import sys
import time
from bs4 import BeautifulSoup
import caluGrade

reload(sys)
sys.setdefaultencoding('utf-8')

#post请求头部
global headers
headers = {}
#请求数据包
global postData
postData = {}

global root_dir 
#root_dir = '/home/innerac/dev/GradeQuery/'
root_dir = '/root/dev/GradeQuery/'
root_ip = "http://202.119.113.135/"

def getCheckCode(url,analyzer):
    # print "+"*20+"getCheckCode"+"+"*20
    response = urllib2.urlopen(url)
    status = response.getcode()
    picData = response.read()
    path = root_dir+"showTest/grade_crawle/tmp/vcode.jpg"
    # path = "../tmp/vcode.jpg"
    if status == 200:
        localPic = open(path, "wb")
        localPic.write(picData)
        localPic.close() 
        result = analyzer.analyze(path)
        if result == None:
            # print "解析失败..."
            postData["v_yzm"] = 'Error'
        else:
            print "解析成功，解析结果：%s"%result
            postData["v_yzm"] = result
    else:
        print "failed to get Check Code, status: ",status

def sendPostData(url, data, header):
    # print "+"*20+"sendPostData"+"+"*20
    data = urllib.urlencode(data)      
    request = urllib2.Request(url, data, header)
    response = urllib2.urlopen(request)
    text = response.read().decode("gbk")
    info = response.info()
    status = response.getcode()
    response.close()
    # print status
    # print info


    key = '学分制综合教务'
    if key in text:
        print 'Login Successful !!'
        return True
    else:
        print 'Login Failed ...'
        return False
    # print "Response:", text

def login(login_url, vcode_url, postData, headers,analyzer):
    cookiejar = cookielib.LWPCookieJar()#LWPCookieJar提供可读写操作的cookie文件,存储cookie对象
    cookieSupport= urllib2.HTTPCookieProcessor(cookiejar)
    opener = urllib2.build_opener(cookieSupport, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    #打开登陆页面
    urllib2.urlopen(login_url)
    #此时直接发送post数据包登录
    getCheckCode(vcode_url,analyzer)
    success_test, failed_test = 0, 0
    return sendPostData(login_url, postData, headers)

def getHtml(url):
    page = urllib2.urlopen(url)
    html = page.read().decode("gbk")
    return html

def is_login(uid,pwd):
    # print "初始化分类器..."
    segmenter = NormalSegmenter()
    extractor = SimpleFeatureExtractor( feature_size=20, stretch=False )

    analyzer = KNNAnalyzer( segmenter, extractor)
    analyzer.train(root_dir+'showTest/grade_crawle/data/features.jpg')
    # analyzer.train('../data/features.jpg')

    # print "开始模拟登录..."
    login_url = root_ip+"loginAction.do"
    vcode_url = root_ip+'validateCodeAction.do?random=0.2583906068466604'

    #post请求头部
    global headers
    global postData
    headers = {
        'x-requestted-with': 'XMLHttpRequest',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate',
        'ContentType': 'application/x-www-form-urlencoded; chartset=UTF-8',
        'Host':    'login.taobao.com',
        'DNT': 1,
        'Cache-Control': 'no-cache',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',  
        'Referer' : 'https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fwww.taobao.com%2F',
        'Connection' : 'Keep-Alive'
    }
    #用户名，密码
    username = uid
    password = pwd
    #请求数据包
    postData = {   
        'zjh':username, 
        'mm':password,             
    }

    test_number = 5

    while login(login_url,vcode_url,postData,headers,analyzer) == False:
        test_number -= 1
        if(test_number == 0):
            print "please check out your uid and password!!"
            break;
    if test_number <= 0:
        return False
    return True
    
    
def getSource(check):

    all_url = root_ip+"gradeLnAllAction.do?type=ln&oper=sxinfo&lnsxdm=001"
    now_url = root_ip+"bxqcjcxAction.do"
    year_2015 = root_ip+"gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2012-2013%D1%A7%C4%EA1(%C1%BD%D1%A7%C6%DA)"
    year_1516 = root_ip+"gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2015-2016%D1%A7%C4%EA1(%C1%BD%D1%A7%C6%DA)"
    # select
    if check == 'all' or check == 'inter':
        url = all_url
    elif check == '1415' or check == '1314':
        url = year_2015
    elif check == 'one':
        url = now_url
    elif check == '15161':
        url = year_1516
    page = getHtml(url)
    page = page.encode('utf-8')
    if check == '1415':
        tmp_x = page.find("<a name=\"2014-2015")
        tmp_y = page.find("<a name=\"2015-2016")
        page = page[tmp_x:tmp_y]
    if check == '1314':
        tmp_x = page.find("<a name=\"2013-2014")
        tmp_y = page.find("<a name=\"2014-2015")
        page = page[tmp_x:tmp_y]
    if check == '15161':
        tmp_x = page.find("<a name=\"2015-2016")
        page = page[tmp_x:]
    soup = BeautifulSoup(page)
    trs = soup.findAll('tr',{'class':'odd'})
    lists = []
    for tr in trs:
        ll = []
        tds = tr.findAll('td')
        for td in tds:
            tmp = ''
            if(td.p):
                tmp = td.p.string.strip().encode('utf-8')
            else:
                tmp = td.string.strip().encode('utf-8')
            # print tmp
            ll.append(tmp)
        lists.append(ll)
    
    subjects = [] 
    rsubjects = []   

        # select
    if (check == 'all' or check == '1415' or check == '1314' or check == 'inter' or check == '15161'):
        if check == 'inter':
            tmp_bool = True
        else:
            tmp_bool = False
        for list in lists:
		subject = []
		if(list[5] == '\xe5\xbf\x85\xe4\xbf\xae' or tmp_bool):
			rsubjects.append([list[2],list[4],list[6]]) 
			subject.append(list[4])
			subject.append(list[6])
			subjects.append(subject)
    elif check == 'one':
        for list in lists:
		subject = []
		if(list[5] == '\xe5\xbf\x85\xe4\xbf\xae'):
			rsubjects.append([list[2],list[4],list[9]]) 
			subject.append(list[4])
			subject.append(list[9])
			subjects.append(subject)


    
    credit = caluGrade.get_credit(subjects)
    rsubjects.insert(0,credit)
    return rsubjects
