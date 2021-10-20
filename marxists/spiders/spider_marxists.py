#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File        :   spider_marxists.py
@Build_time  :   2021/09/24 11:06:30
@Author      :   東篱
@Version     :   1.0
@Descroption :   
'''

from utils import Utils
import scrapy
from alive_progress import alive_bar
from scrapy.http import Request
from bs4 import BeautifulSoup


from ..items import MarxistsItem


class SpiderMarxistsSpider(scrapy.Spider):
    name = 'spider_marxists'
    allowed_domains = ['marxists.org']
    # start_urls = ['https://www.marxists.org/chinese/maozedong/index.htm']

    with open('urls.txt', 'r', encoding='utf-8') as f:
        start_urls = f.read().splitlines()

    # start_urls = ['https://www.marxists.org/chinese/maozedong/marxist.org-chinese-mao-19460806.htm']

    html_save_path = "tmp\\"

    def parse(self, response):
        item = MarxistsItem()
        # 文章标题
        # title = response.xpath('//*[@class="title1"]/text()').get()
        # if title is None:
        title = response.xpath('/html/body/p[1]//text()').getall()
        # if title is None:
        #     title = response.xpath('/html/body/p/font//text()').getall()

        item['article_title'] = ''
        for t in title:
            item['article_title'] += t

        # 文章的顺序
        url = response.url
        item['article_index'] = self.start_urls.index(response.url)

        item['article_url'] = response.url

        # 文章内容, 待清洗的网页内全部文本
        soup = BeautifulSoup(response.text, "html5lib")
        item['soup'] = soup

        print("{0:03d}_{1}{2}".format(item['article_index'], item['article_title'], url))

        # 获取注释
        notes_href = response.xpath('//*[starts-with(@name, "_ftnref")]/@href').getall()
        notes_index = Utils.clean_list(response.xpath('//*[starts-with(@name, "_ftnref")]//text()').getall())
        item['notes_index'] = notes_index
        item['notes_text'] = []
        for note_href in notes_href:
            xpath = '//*[@name="{}"]/following-sibling::text()[1]'.format(note_href[1:])
            note_text = response.xpath(xpath).get()
            note_text = Utils.clean_str(note_text)
            note_img = '<img alt="{}" class="duokan-footnote" id="{}" src="../Images/note_original.png" />'.format(note_text, Utils.gen_id(8))
            note_text = BeautifulSoup(note_img, 'html5lib').img.prettify(formatter='html5lib')
            item['notes_text'].append(note_text)

        item['notes'] = dict(zip(item['notes_index'], item['notes_text']))
        return item
