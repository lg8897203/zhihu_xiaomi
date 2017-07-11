# -*- coding: utf-8 -*-

##this is for questions

from scrapy import Spider, Request
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient

class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    host = 'https://www.zhihu.com'
    xiaomi_urls = 'https://www.zhihu.com/topic/19626175/questions?page={page}'


    moclient = MongoClient ()
    moclient = MongoClient ('192.168.7.16', 27017)
    #moclient = MongoClient ('localhost', 27017)
    db = moclient.zhihu_xiaomi
    db.collection_names (include_system_collections=False)

    def start_requests(self):
        for i in range(1,764):
            print(i)
            yield Request(self.xiaomi_urls.format(page=i), self.parse)


    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        questions = soup.select('.question-item')
        for result in questions:
            answerCount = result.select('meta')[0]['content']
            res = result.select('.question-item-title')
            timestamp = res[0].select('span')[0]['data-timestamp']
            question = res[0].select('a')[0]
            url = self.host+question['href']
            title = question.text
            qid = question['href'].split('/')[2]
            #print(answerCount,timestamp,url,title,qid)

            self.db.test.insert({"qid":qid,"title":title,"answerCount":answerCount,"url":url,"timestamp":timestamp,"type":"question"})