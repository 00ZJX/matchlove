# -* encoding:utf-8 *-
__author__ = 'zjx'
# python 2.7.9

import pymongo
import gridfs
import re
import bs4

conn = pymongo.MongoClient("localhost",27017)
db0 = conn.MongoDB_html
db1 = conn.MongoDB_html_b
gfs = gridfs.GridFS(db1,'match_com_tw')
db2 = conn.MongoDB_json
gfs0 = gridfs.GridFS(db0,'match_com_tw')
gfs1 = gridfs.GridFS(db1,'match_com_tw')
# 转移数据
# 如果存在，卸载MongoDB_html_b数据库及MongoDB_json数据库
"""
if db1:
    conn.drop_database(db1)
    print "MongoDB_html_b已删除"
"""
if db2:
    conn.drop_database(db2)
    print "MongoDB_json已删除"

print db1.collection_names()
print db2.collection_names()

def cope_database(db0,db1):
    for u in db0.match_com_tw.files.find():
        i = u['_id']
        print i
        persion_url = u['url']
        print persion_url
        filename = u['filename']
        print filename
        persion_html = gfs0.get(i).read()
        gfs1.put(data=persion_html, filename=filename, uid=i, url=persion_url, _id=i)
        i = str(i)
        print "_id为"+i+"已转存"
    count0 = db0.match_com_tw.files.count()
    count1 = db1.match_com_tw.files.count()
    if count0 == count1:
        print "数据库复制成功！"
        print "*"*100
    else:
        print "数据复制出错！"
# cope_database(db0,db1)
print db1.collection_names()

# 更新数据
db1.match_com_tw.files.update({},{'$set':{'analyse':0}},upsert=False,multi=True)
print "更新db1数据为analyse:0成功！"
print db1.match_com_tw.files.find_one()
# 提取内容
def get_page_text(html): #提取文本模块
    soup = bs4.BeautifulSoup(html)
    t = soup.get_text()
    t = t.replace("\t","").replace("\n","").replace("\r","").replace(" ","")
    print t
    r = re.compile(u"相親基本資料(.*?)功能說明")
    list = r.findall(t) # 返回的是元组
    text = list[0] + u"·"
    print "获取文本成功"
    return text
def draw():
    print "*"*100
    for u in db1.match_com_tw.files.find():
        i = u['_id']
        filename = u['filename']
        persion_url = u['url']
        persion_html = gfs1.get(i).read()
        i = str(i)
        print "已获取_id"+i+"个人主页"
        text = get_page_text(persion_html)
        print text
        db2.match_com_tw.info.save({"_id":i,"filename":filename,"url":persion_url,})
        print "提取文本……"
        fp = open('rules.txt','r')     # 打开匹配规则文件
        print "获取匹配规则……"
        for rule in fp.readlines():

            # 以行为单位提取规则
            r = re.compile(r"\"(.*?)\"")
            property = r.search(rule)  # 获取属性 （相当于MongoDB_json的key）
            r = re.compile(r",(.*?):")
            pname = r.search(rule)    # 获取属性名
            r = re.compile(r"<(.*?)>")
            prule = r.search(rule)    # 获取规则（正则表达式匹配）
            u_prule = unicode(prule.group(1),encoding='utf-8')  # 对规则进行编码
            r = re.compile(u_prule)
            result = r.search(text)   #匹配个人信息,返回的是匹配对象
            print "属性：" + property.group(1)
            property = property.group(1)
            print "项目：" + pname.group(1)
            pname = pname.group(1)
            print "结果：",result.group(1)
            result = result.group(1)
            result = result.strip()
            print result
            print "存数据库"
            db2.match_com_tw.info.update({"_id":i},{"$set":{property:{pname:result}}})
        db1.match_com_tw.files.update({"_id":i},{'$set':{'analyse':1}})
        print "_id：" +i+ "分析完成"
        print "\n"
    print "*"*100


draw()