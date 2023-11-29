# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
# from django.contrib.auth.models import User
# from mongoengine import *
from django.urls import reverse
from django.utils.text import slugify
from django.db import models

from django.conf import settings
# from bson.objectid import ObjectId
# import pymongo
import re

class FileItem():
    urlPath=""
    name = ""
    fileType = ""
    size = ""
    createDate = ""
    icon=""

    def __init__(self,urlPath,name, fileType, size,createDate,icon):
        self.urlPath=urlPath;
        self.name = name;
        self.fileType = fileType;
        self.size = size;
        self.createDate = createDate;
        self.icon=icon;

class FileUrlPath():
    displayPath=""
    urlPath="";
    '''
    页面显示层级的路径
    '''
    def __init__(self,displayPath="显示的地址",urlPath="URL地址"):
        self.displayPath=displayPath
        self.urlPath=urlPath;


class DownFileItem():
    '''
    下载文件的目录结构
    '''
    version="";
    comment="";
    size="";
    date="";
    downUrl="";

    def __init__(self, version, comment, size, date,downUrl):
        self.version=version;
        self.comment=comment;
        self.size=size;
        self.date=date;
        self.downUrl=downUrl;



class Fujian(models.Model):
    name = models.CharField(max_length=32,verbose_name="附件名称")
    file = models.FileField(upload_to="upload/%Y/%m/%d/")
    # uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


# Create your models here.
#页面模板
class PageModel(models.Model):
    # id = models.ForeignKey('id',  on_delete=models.CASCADE);#模型id(id)
    ename=models.CharField(max_length=50);#模型英文名(ename)
    cname=models.CharField(max_length=50);#模型英文名(cname)
    path=models.CharField(max_length=50);#模型路径(path)



#页面内容
class ArticleContext(models.Model):
    # _id = models.CharField(max_length=50);#文章id(id)
    # articleid = models.CharField(db_column='article_id',max_length=50)
    totallevel = models.CharField(db_column='total_level',max_length=50);#total显示(totalLevel)
    typeid = models.CharField(db_column='type_id',max_length=50);#所属版块id(typeid)  typeid=1 资讯内容   typeid=2 政策动态 typeid=3 各地政策汇总
    modelid = models.CharField(db_column='model_id',max_length=50);#所属模型id(modelid)
    arcrank = models.CharField(db_column='arcrank',max_length=50);#排序(arcrank)
    click = models.CharField(db_column='click',max_length=50);#点击(click)
    title = models.CharField(db_column='title',max_length=50);#文章标题(title)
    shortitle = models.CharField(db_column='shor_title',max_length=50);#文章短标题(shortitle)
    writer = models.CharField(db_column='writer',max_length=50);#作者(writer)
    resource = models.CharField(db_column='resource',max_length=50);#来源(resource)
    updatedate = models.CharField(db_column='update_date',max_length=50);#更新时间(updatedate)
    sendate = models.CharField(db_column='send_date',max_length=50);#发表时间(sendate)
    keywords = models.CharField(db_column='keywords',max_length=50);#关键词(keywords)
    content = models.CharField(db_column='content',max_length=50);#文章正文(content)
    contentimg1 = models.CharField(db_column='content_img1',max_length=50);#正文图片(contentimg1)
    titleimg1 = models.CharField(db_column='title_img1',max_length=50);#标题图片(titleimg1)

    class Meta:
        db_table = "article_context"
        ordering = ('typeid',)
        # index_together = (('articleid'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse('product_detail', args=[str(self.title)])
        return reverse('newsDetail', kwargs={'title': self.title})


    # meta = {'collection': 'ArticleContext'}

    # def __str__(self):
    #     return self.title

    # def __init__(self):
    #     '''初始化'''
    #     # 连接 mongo 数据库，获得数据指定集合
    #     self.client = pymongo.MongoClient('mongodb://%s:%s@%s:%d/%s' % (settings.
    #                                                                     MONGO_USER, settings.MONGO_PWD,
    #                                                                     settings.MONGO_HOST, settings.MONGO_PORT,
    #                                                                     settings.
    #                                                                     MONGO_AUTHDB))[settings.MONGO_DBNAME]
    #     self.articlesContext = self.client['ArticleContext']
    #
    # def find_one(self, id):
    #     '''获取指定数据'''
    #     article = self.articlesContext.find_one({"_id": ObjectId(id)})
    #     return article
    #
    # def find_by_title(self, title):
    #     '''获取指定数据'''
    #     article = self.articlesContext.find_one({"title": title})
    #     return article
    #
    # #默认显示资讯内容
    # def find_all(self,typeid=1):
    #     '''返回全部文章'''
    #     '''默认按照倒序排列，即取出最新插入的文章'''
    #     article_list = self.articlesContext.find({"typeid": typeid}).sort('_id', pymongo.DESCENDING)
    #     return article_list
    #
    # #默认显示资讯内容
    # def find_alltype(self,keywords):
    #     '''返回全部文章'''
    #     '''默认按照倒序排列，即取出最新插入的文章'''
    #     if keywords is None or keywords == '':
    #         article_list = self.articlesContext.find().sort('typeid', pymongo.DESCENDING)
    #     else:
    #         rgx = re.compile('.*'+keywords+'.*')  # compile the regex
    #         article_list = self.articlesContext.find({"content": rgx}).sort('typeid', pymongo.DESCENDING)
    #
    #     return article_list
    #
    # def updateNews(self,articleContextForm):
    #     '''更新新闻内容'''
    #     if articleContextForm == None:
    #         raise Exception('请提供  参数!')
    #     myquery = {"title": articleContextForm.data['title']}
    #     newvalues = {"$set":
    #                      {
    #                          "totallevel": articleContextForm.data['totallevel'],
    #                          "typeid": articleContextForm.data['typeid'],
    #                          "modelid": articleContextForm.data['modelid'],
    #                          "arcrank": articleContextForm.data['arcrank'],
    #                          "click": articleContextForm.data['click'],
    #                          "shortitle": articleContextForm.data['shortitle'],
    #                          "resource": articleContextForm.data['resource'],
    #                          "updatedate": articleContextForm.data['updatedate'],
    #                          "sendate": articleContextForm.data['sendate'],
    #                          "keywords": articleContextForm.data['keywords'],
    #                          "contentimg1": articleContextForm.data['contentimg1'],
    #                          "titleimg1": articleContextForm.data['titleimg1']
    #                       }
    #                  }
    #     self.articlesContext.update_one(myquery,newvalues)
    #
    # def updateRead(self, id=None, cnt=1):
    #     '''阅读量+1'''
    #     if id == None:
    #         raise Exception('请提供 id 参数!')
    #     self.articlesContext.update_one({'_id': ObjectId(id)}, {'$inc': {'read': cnt}})
    #
    # def find_recommendArticle(self, labels):
    #     '''根据用户的兴趣label选择文章序列并返回'''
    #     # labels按照值降序排列，放在label_list中
    #     label_list = sorted(labels.items(), key=lambda e: e[1], reverse=True)
    #     # 只取前5个兴趣label
    #     if len(label_list) > 5:
    #         label_list = label_list[0:5]
    #     # 返回用户感兴趣的所有文章
    #     # article_C 为放置各个分类文章的容器
    #     article_C = []
    #     for category in label_list:
    #         article_C.append((self.articlesContext.find({'category': category[0]}).sort('_id', pymongo.DESCENDING)))
    #     return article_C
    #
    # def find_labelArticle(self, label):
    #     '''返回单个label的文章列表'''
    #     article_list = self.articlesContext.find({'category': label}).sort('_id', pymongo.DESCENDING)
    #     return article_list
    #
    # def updateUpvote(self, id=None):
    #     '''点赞接口'''
    #     if id == None:
    #         raise Exception('请提供 id 参数!')
    #     self.articlesContext.update_one({'_id': ObjectId(id)}, {'$inc': {'upvote': 1}})
