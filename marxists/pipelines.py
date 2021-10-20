#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File        :   pipelines.py
@Build_time  :   2021/09/24 16:12:19
@Author      :   東篱
@Version     :   1.0
@Descroption :   
'''

from utils import Utils
from bs4 import BeautifulSoup


class MarxistsPipeline:
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):

        # 清洗item数据
        if item['article_title']:
            item['article_title'] = Utils.clean_str(item['article_title'])

        item['xhtml_items'] = self.analyse_soup(item)
        return item

    def close_spider(self, spider):
        pass

    def analyse_soup(self, item):
        soup = item['soup']
        xhtml_items = []
        print("test")

        # 用于判断文章是否开始, 跳过html开头的内容
        start_sign = False
        # 用于判断正文是否开始
        text_start_sign = False
        for child in soup.body.children:
            # 遍历子节点
            if child.name == 'span':
                # 跳过注释
                continue
            if child.name is None and Utils.clean_str(child.string) == '':
                # 空行
                continue
            try:
                if  Utils.clean_str(str(child.get_text())) == item['article_title']:
                        start_sign = True
                        s = '<h2 class="chapter-title-center"><a href="{}"></a></h2>'.format(item['article_url'])
                        new_title = BeautifulSoup(s, 'html5lib').h2
                        new_title.a.string = Utils.clean_str(str(child.get_text()))
                        xhtml_items.append(new_title)
                        continue
            except Exception:
                pass
            # try:
            #     if 'title1' in child['class']:
            #         # 文章标题
            #         start_sign = True
            #         s = '<h2 class="chapter-title-center"></h2>'
            #         new_title = BeautifulSoup(s, 'html5lib').h2
            #         new_title.string = child.get_text()
            #         xhtml_items.append(new_title)
            #         continue
            # except Exception:
            #     pass
            if not start_sign:
                # 文章未开始
                continue

            try:
                if child.name == 'p' and 'center' in child['align'] and not text_start_sign:
                    # 章前引语
                    s = '<div class="body-quotation-background3"><p></p></div>'
                    new_quotation = BeautifulSoup(s, 'html5lib').div
                    new_quotation.p.string = Utils.clean_str_all(child.get_text())
                    xhtml_items.append(new_quotation)
                    text_start_sign = True
                    continue
            except Exception:
                pass

            try:
                if child.name == 'b' and not text_start_sign:
                        # 副标题
                        s = '<p class="bodycontent-text-center-kai"></p>'
                        new_date_title = BeautifulSoup(s, 'html5lib').p
                        new_date_title.string = child.get_text()
                        xhtml_items.append(new_date_title)
                        continue
            except Exception:
                pass

            try:
                if 'date' in child['class']:
                    # 副标题
                    s = '<p class="bodycontent-text-center-kai"></p>'
                    new_date_title = BeautifulSoup(s, 'html5lib').p
                    new_date_title.string = child.get_text()
                    xhtml_items.append(new_date_title)
                    continue
            except Exception:
                pass

            try:
                if 'a1' in child['class']:
                    # 章前引语
                    s = '<div class="body-quotation-background3"><p></p></div>'
                    new_quotation = BeautifulSoup(s, 'html5lib').div
                    new_quotation.p.string = Utils.clean_str_all(child.get_text())
                    xhtml_items.append(new_quotation)
                    text_start_sign = True
                    continue
            except Exception:
                pass

            try:
                if 'a3' in child['class']:
                    # 引文段落
                    s = '<p class="reference-text"></p>'
                    new_blockquote = BeautifulSoup(s, 'html5lib').p
                    new_blockquote.string = Utils.clean_str(child.get_text())
                    xhtml_items.append(new_blockquote)
                    continue
            except Exception:
                pass

            try:
                if child.name is None or child.name in ['b']:
                    # 正文
                    text_start_sign = True

                    if str(child.string).replace('\n', '').startswith('（'):
                        class_ = 'bodycontent-text-both'
                    elif not str(child.string).replace('\n', '').startswith('\u3000'):
                        class_ = 'bodycontent-text-left0'
                    else:
                        class_ = 'bodycontent-text-both'

                    if child.previous_sibling.name in [None, 'br', 'h3', 'h4', 'h5']:
                        # 另起一段
                        new_text = BeautifulSoup(
                            '<p class="{}">'.format(class_), 'html5lib').p
                        new_text.string = Utils.clean_str(str(child.string))
                        xhtml_items.append(new_text)
                        continue
                    else:
                        # 接上文
                        new_text = BeautifulSoup(
                            str(xhtml_items[-1]), "html5lib").p
                        new_text.string += Utils.clean_str(str(child.string))
                        xhtml_items[-1] = new_text
            except Exception:
                pass

            try:
                if child.name == 'blockquote':
                    if not text_start_sign:
                        # 章前引语
                        s = '<div class="body-quotation-background3"><p></p></div>'
                        new_quotation = BeautifulSoup(s, 'html5lib').div
                        new_quotation.p.string = Utils.clean_str_all(child.get_text())
                        xhtml_items.append(new_quotation)
                        text_start_sign = True
                        continue
                    if text_start_sign:
                        # 引文段落
                        s = '<p class="reference-text"></p>'
                        new_blockquote = BeautifulSoup(s, 'html5lib').p
                        new_blockquote.string = Utils.clean_str(child.get_text())
                        xhtml_items.append(new_blockquote)
                        continue
            except Exception:
                pass

            if child.name == 'h3':
                text_start_sign = True
                id = Utils.gen_id(8)
                s = '<h3 class="title2"><a id="{}"></a><br /></h3>'.format(id)
                new_title3 = BeautifulSoup(s, 'html5lib').h3
                new_title3.a.string = Utils.clean_str(child.get_text())
                xhtml_items.append(new_title3)
                continue
            if child.name == 'h4':
                text_start_sign = True
                s = '<h4 class="title3"><br /></h4>'
                new_title4 = BeautifulSoup(s, 'html5lib').h4
                new_title4.string = Utils.clean_str(child.get_text())
                xhtml_items.append(new_title4)
                continue
            if child.name == 'h5':
                text_start_sign = True
                s = '<p class="bodycontent-text-left0"><span class="bold"></span></p>'
                new_title5 = BeautifulSoup(s, 'html5lib').p
                new_title5.span.string = Utils.clean_str(child.get_text())
                xhtml_items.append(new_title5)
                continue
            if child.name == 'a':
                # 注释
                a = BeautifulSoup(str(xhtml_items[-1]), "html5lib")
                a = a.body.contents[0]
                a.string += Utils.clean_str(child.get_text())
                xhtml_items[-1] = a
                continue
            try:
                if child.name == 'p' and 'right' in child['align']:
                    # 落款
                    s = '<p class="signature"></p>'
                    new_signature = BeautifulSoup(s, 'html5lib').p
                    new_signature.string = Utils.clean_str(child.get_text())
                    xhtml_items.append(new_signature)
            except Exception:
                pass
        return xhtml_items


class GenXHTMLPipeline:
    xhtml_path = 'xhtml\\'
    xhtml_path = 'tmp\\'

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        xhtml = '''<?xml version="1.0" encoding="utf-8" standalone="no"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n\n<html xmlns="http://www.w3.org/1999/xhtml">\n<head>\n    <title>{}</title>\n    <link href="../Styles/stylesheet.css" rel="stylesheet" type="text/css" />\n</head>\n\n    <body>\n'''.format(item['article_title'])

        new_soup = BeautifulSoup(xhtml, "html5lib")
        xhtml_items = item['xhtml_items']
        for xhtml_item in xhtml_items:
            xhtml_item = str(xhtml_item)
            xhtml_soup = BeautifulSoup(xhtml_item, "html5lib").body.contents[0]
            new_soup.body.append(xhtml_soup)
        new_soup = str(new_soup)
        notes_index = item['notes_index']
        notes = item['notes']
        for note_index in notes_index:
            new_soup = new_soup.replace(note_index, str(notes[note_index]).replace('\n', ''))

        with open('{0}{1:03d}_{2}.xhtml'.format(self.xhtml_path, item['article_index'], Utils.gen_id(16)), 'w', encoding="utf-8") as f:
            f.write(str(new_soup))
        return item

    def close_spider(self, spider):
        pass
