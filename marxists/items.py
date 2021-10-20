#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File        :   items.py
@Build_time  :   2021/09/24 11:04:20
@Author      :   東篱
@Version     :   1.0
@Descroption :   
'''


import scrapy


class MarxistsItem(scrapy.Item):
    # define the fields for your item here like:
    article_url = scrapy.Field()           # 文章链接
    article_title = scrapy.Field()         # 文章标题
    article_index = scrapy.Field()         # 文章的顺序
    notes_index = scrapy.Field()           # 注释索引
    notes_text = scrapy.Field()            # 注释内容
    notes = scrapy.Field()                 # 注释字典
    soup = scrapy.Field()                  # BeautifulSoup文件
    xhtml_items = scrapy.Field()           # 生成的xhtml文件的组成元素