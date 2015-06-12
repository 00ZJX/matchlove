
# -* encoding:utf-8 *-
# python 2.7.9
__author__="zjx"

import urllib2,urllib,re
import cookielib
import bs4

# 设置cookie
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

# 初始化数据
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko}Chrome/41.0.2272.118 Safari/537.36'}
member_url = "http://www.matchlove.com.tw/user/index.php"
sex1_search_url = "http://www.matchlove.com.tw/match-search.php?sex=1"
sex2_search_url = "http://www.matchlove.com.tw/match-search.php?sex=2"

# 模拟登录
def login():
    login_url = "http://www.matchlove.com.tw/loginIndex1.php?act=login"
    login_data = {
        'username':'',
        'password':'',
        'remember':'1'
    }
    data = urllib.urlencode(login_data)
    try:
        request = urllib2.Request(url=login_url,data=data,headers=headers)
        html = urllib2.urlopen(request).read()
        return html
    except Exception,e:
        print e
        login()

# 获取页面
def get_html(url):
    request  = urllib2.Request(url=url,headers=headers)
    html = urllib2.urlopen(request).read()
    return html

# 获取登录后会员首页
def get_member_html():
    member_url = "http://www.matchlove.com.tw/user/index.php"
    try:
        request  = urllib2.Request(url=member_url,headers=headers)
        html = urllib2.urlopen(request).read()
        return html
    except Exception,e:
        print e
        get_member_html()

# 打开搜索页
def search_sex1_html():
    sex1_search_url = "http://www.matchlove.com.tw/match-search.php?sex=1"
    try:
        sex1_request = urllib2.Request(url=sex1_search_url,headers=headers)
        search_sex1_html = urllib2.urlopen(sex1_request).read()
        return search_sex1_html
    except Exception,e:
        print e

def search_sex2_html():
    sex2_search_url = "http://www.matchlove.com.tw/match-search.php?sex=2"
    try:
        sex2_request = urllib2.Request(url=sex2_search_url,headers=headers)
        search_sex2_html = urllib2.urlopen(sex2_request)
        search_sex2_html = search_sex2_html().read()
        return search_sex2_html
    except Exception,e:
        print e


#男女搜索页面
def search_sex1_post():
    sex1_search_url = "http://www.matchlove.com.tw/match-list.php?sex=1"
    postdata = {
          'Drinking':'0',
          'eat':'0',
          'smoking':'0',
          'submit':'立即搜尋'}
    data = urllib.urlencode(postdata)
    try:
        request = urllib2.Request(sex1_search_url,data,headers)
        html = urllib2.urlopen(request).read()
        return html
    except Exception,e:
        print e
        search_sex1_post()


def search_sex2_post():
     sex2_search_url = "http://www.matchlove.com.tw/match-list.php?sex=2"
     postdata = {
          'Drinking':'0',
          'eat':'0',
          'smoking':'0',
          'submit':'立即搜尋'}
     data = urllib.urlencode(postdata)
     try:
         request = urllib2.Request(sex2_search_url,data,headers)
         html = urllib2.urlopen(request).read()
         return html
     except Exception,e:
         print e
         search_sex2_post()

# 获取下一页
def get_next_persion_list():
    html = open("persion_list.txt","r").read()
    soup = bs4.BeautifulSoup(html)
    a = soup.select('a')
    for i in a:
        if i.text== u"下一頁":
            url_half = i['href']
            print url_half
            break


# 写入文件
def input_file(filename,filecontens,mode):    #将文件写入到txt文档中缓存
     if mode == 'a':
          output = open(filename, 'a')
          output.write(filecontens)
          output.close( )
     if mode == 'w':
          output = open(filename, 'w')
          output.write(filecontens)
          output.close()
     if mode == "r+":        #清空文件
          fs = open(filename,"r+")
          fs.truncate()
          fs.close()
     if mode == "r":
          fs = open(filename,"r")
          html = fs.read()
          fs.close()
          return html
     if mode == "r+a":
         fs = open(filename,"r+")
         fs.truncate()
         fs.close()
         output = open(filename, 'a')
         output.write(filecontens)
         output.close( )
     return

# 获取用户的uid
def get_persion_uid(x,sex):
    contents = open("./txt/"+sex+"/persion_list/persion_list"+x+".txt","r").read()
    c = re.compile(u'<td class="tdOrderNum"  >(.*?)</td>')
    result = c.findall(contents)
    text = str(result)
    print "在写入第"+x+"页uid"
    input_file("./txt/"+sex+"/persion_list/persion_list"+x+"_uid.txt",text,"w")
    input_file("./html/"+sex+"/persion_list/persion_list"+x+"_uid.txt",text,"w")
    return result

# get list page num
import urlparse
def get_list_num(html):
    soup = bs4.BeautifulSoup(html)
    a = soup.select('a')
    for i in a:
        if i.text== u"尾頁":
            url_half = i['href']
            query = urlparse.urlparse(url_half).query
            d = dict([(k,v[0]) for k,v in urlparse.parse_qs(query).items()])
            num = d['page']
            return num


import socket
timeout = 30
socket.setdefaulttimeout(timeout)

import threading
import multiprocessing

import time

def get_i(i, sex):
    persion_url = "http://www.matchlove.com.tw/match-love.php?userid="+i
    print "用户的url为："+persion_url
    print "&"*20
    try:
        persion_html = urllib2.urlopen(persion_url)
        persion_html = persion_html.read()
        print "在写入用户"+i+"的个人页面"
        filename = sex+"sex"+i+".html"
        input_file("./html/"+sex+"/persion_html/persion_html"+i+".html",persion_html,"w")
        input_file("./txt/"+sex+"/persion_txt/persion_txt"+i+".txt",persion_html,"w")
        print "开始写入数据库！"
        file_id = put_file(persion_html,filename,i,persion_url)
        print file_id
    except Exception,e:
        print e
        time.sleep(30)
        print "网络出现问题，正在尝试再次请求....."
        print "重新抓取用户"+i+"的个人主页"
        get_i(i, sex)



def get_persion_html(result):
    for i in result:
        print "正在获取用户"+i+"的个人主页"
        get_i(i, sex)
        print ""*50
    print "#"*30


# 打开下一页的数据
def get_persion_list_html(x, sex):
    persion_list_url = "http://www.matchlove.com.tw/match-list.php?sex="+sex+"&page="+x+"&by=&order="
    print "在爬取的url为："+persion_list_url
    try:
        html = urllib2.urlopen(persion_list_url)
        content = html.read()
        print "在写入第"+x+"列表页"
        input_file("./html/"+sex+"/persion_list/persion_list"+x+".html",content,"w")
        input_file("./txt/"+sex+"/persion_list/persion_list"+x+".txt",content,"w")
    except Exception,e:
        print e
        time.sleep(30)
        print "网络出现问题，正在尝试再次请求....."
        print "当前页面为："+persion_list_url
        get_persion_list_html(x, sex)


import pymongo
import gridfs
def conn_mongodb():
    print "开始连接数据库"
    try:
        conn = pymongo.MongoClient("",27017)
        db0 = conn.MongoDB_html_c
    except Exception,e:
        print e
    return db0

# 上传文件
def put_file(persion_html,filename,i,persion_url):
    fs = gridfs.GridFS(db0,'match_com_tw')
    """
    for u in conn.match_com_tw.find():
        id = u['_id']
        if i == id:
            print "文件已存在！此处跳过！"
        else:
            file_id = fs.put(data=persion_html, filename=filename, uid=i, url=persion_url, _id=i)
            return file_id
            """
    try:
        file_id = fs.put(data=persion_html, filename=filename, uid=i, url=persion_url, _id=i)
        return file_id
    except Exception,e:
        print e
        print "文件已存在！此处跳过！"



def get_sex1():
    print "*"*100
    print "开始获取sex = 1 的数据"
    search_sex1_html()
    html = search_sex1_post()
    num = get_list_num(html)
    num = int(num)
    return num

def get_sex2():
    print "*"*100
    print "开始获取sex = 2 的数据"
    search_sex2_html()
    html = search_sex2_post()
    num = get_list_num(html)
    num = int(num)
    return num


import Queue
import threading
import time
class spider_thread(threading.Thread):
    def __init__(self,queue,sex):
        threading.Thread.__init__(self)
        self.queue = queue
        self.queue = sex


    def run(self):
        while(queue.empty() == False):
            x = queue.get()
            print x
            x = str(x)
            print "正在抓取第"+x+"页"
            get_persion_list_html(x, sex)
            print "获取第"+x+"页uid"
            result = get_persion_uid(x, sex)
            get_persion_html(result)
            print "获取第"+x+"页结束"
            print "*"*100
            x = int(x)
            x = x+1
        print time.localtime()

import sys
import socket

def client():
    s = socket.socket()
    port = 1235
    try:
        s.connect(("",port))
        x = s.recv(port)
    except Exception,e:
        print e
        sys.exit()
    if x=="You can't get the task":
        s.close()
        print "Task have stop"
    else:
        s.close()
        x = int(x)
        return x
    # sys.exit()


def super_spider():
    x =  client()
    if isinstance(x,int) == True:
        y = x+7
        spider(x,sex,y)
        super_spider()
            # spider(x,sex)
        # spider(queue,sex)
    print "全部完成！^_^"
    """
    for i in range(8):
        spider_salve = spider_thread(queue,sex)
        spider_salve.deame = True
        spider_salve.start()
    """

def spider(x, sex,y):
    while x <= y:
        x = str(x)
        print "正在抓取第"+x+"页"
        get_persion_list_html(x, sex)
        print "获取第"+x+"页uid"
        result = get_persion_uid(x, sex)
        get_persion_html(result)
        print "获取第"+x+"页结束"
        print "*"*100
        x = int(x)
        x = x+1
    # print "sex = "+sex+"全部提取结束^_^"
if __name__ =="__main__":
    start = time.time()
    print time.localtime()
    queue = Queue.Queue()

    login()
    db0 = conn_mongodb()
    num = get_sex1()
    print "共有",num,"页"
    sex = "1"
    # mutex = threading.Lock()

    super_spider()
    # queue.join()
    """
    num = get_sex2()
    x = 1
    sex = "2"
    print "共有",num,"页"
    spider(x,sex)
    print "*"*100
    print "全部完成！^_^"
    """
    stop = time.time()
    print stop-start

