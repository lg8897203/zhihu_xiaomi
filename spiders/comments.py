# -*- coding: utf-8 -*-
from scrapy import Spider, Request
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient

class CommentsSpider(Spider):
    name = 'comments'
    allowed_domains = ['www.zhihu.com']
    answer_url = 'https://www.zhihu.com/api/v4/answers/{aid}/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&order=normal&limit={limit}&offset={offset}&status=open'

    moclient = MongoClient ()
    #moclient = MongoClient ('192.168.7.16', 27017)
    moclient = MongoClient ('localhost', 27017)
    db = moclient.zhihu_xiaomi
    db.collection_names (include_system_collections=False)
    posts = db.answers

    def start_requests(self):
        for post in self.posts.find():
            aid = post['aid']
            yield Request(self.answer_url.format(aid=aid, limit=10, offset=0),
                     self.parse)

    def parse(self, response):
        results = json.loads(response.text)
        aid = results.get('paging').get('previous').split('/')[6]
        if 'data' in results.keys():
            for result in results.get('data'):
                created_time = result.get('created_time')
                cid = result.get('id')
                uid = result.get('author').get('member').get('id')
                vote_count = result.get('vote_count')
                content = result.get('content')
                type = result.get('type')

                self.db.test.insert(
                    {"aid": aid, "content": content, "uid": uid, "cid": cid, "created_time": created_time,
                      "voteup_count": vote_count, "type": type})


        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(next_page,
                          self.parse)