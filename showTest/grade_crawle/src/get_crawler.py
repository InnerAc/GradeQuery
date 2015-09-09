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




def getCheckCode(url,analyzer):
    # print "+"*20+"getCheckCode"+"+"*20
    response = urllib2.urlopen(url)
    status = response.getcode()
    picData = response.read()
    path = "/home/innerac/dev/GradeQuery/showTest/grade_crawle/tmp/vcode.jpg"
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

def getSource(uid,pwd,check):
    # print "初始化分类器..."
    segmenter = NormalSegmenter()
    extractor = SimpleFeatureExtractor( feature_size=20, stretch=False )

    analyzer = KNNAnalyzer( segmenter, extractor)
    analyzer.train('/home/innerac/dev/GradeQuery/showTest/grade_crawle/data/features.jpg')
    # analyzer.train('../data/features.jpg')

    # print "开始模拟登录..."
    login_url = "http://202.119.113.135/loginAction.do"
    vcode_url = 'http://202.119.113.135/validateCodeAction.do?random=0.2583906068466604'
    all_url = "http://202.119.113.135/gradeLnAllAction.do?type=ln&oper=sxinfo&lnsxdm=001"
    now_url = "http://202.119.113.135/bxqcjcxAction.do"
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

    # select
    if check == 'all':
        url = all_url
    else:
        url = now_url


    test_number = 5

    while login(login_url,vcode_url,postData,headers,analyzer) == False:
        test_number -= 1
        if(test_number == 0):
            print "please check out your uid and password!!"
            break;
    if test_number <= 0:
        return []
    if test_number > 0:
        page = getHtml(url)
    print test_number
    page = page.encode('utf-8')
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
    if check == 'all':
        for list in lists:
		subject = []
		if(list[5] == '\xe5\xbf\x85\xe4\xbf\xae'):
			rsubjects.append([list[2],list[4],list[6]]) 
			subject.append(list[4])
			subject.append(list[6])
			subjects.append(subject)
    else:
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

if __name__ == '__main__':
    uid = '1206010416'
    pwd = '941024'
    lists = getSource(uid,pwd)
    for list in lists:
        for ll in list:
            print ll,
        print