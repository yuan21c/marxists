#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File        :   test_read_txt.py
@Build_time  :   2021/09/25 11:14:01
@Author      :   東篱
@Version     :   1.0
@Descroption :   
'''

import re

from utils import Utils

txt_list = []
re_txt = re.compile(r'\<.+?\>')
re_header = re.compile(r'h\d+?')
re_signature = re.compile(r'\<p align="right"\>+?\<\/p\>')
with open(r'marxists\tmp\000_致野坂参三.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = Utils.clean_str(line)
        if line is None or line == '':
            # 空行
            continue
        # print(re.findall(re_signature, line))
        if not Utils.startswithchinese(line):
            # 非正文行
            if re.findall(re_header, line):
                # 标题行
                type = re.findall(re_header, line)[0]
                txt = Utils.clean_list(re_txt.split(line))[0]
                txt_list.append({type: txt})
            elif line.startswith(r'<div class="a3">'):
                type = 'reference'
                txt = Utils.clean_list(re_txt.split(line))[0]
                txt_list.append({type: txt})
            elif line.startswith(r'<p align="right">'):
                type = 'signature'
                txt = Utils.clean_list(re_txt.split(line))[0]
                txt_list.append({type: txt})
            else:
                continue
        else:
            # 正文行
            type = "txt"
            txt = Utils.clean_list(re_txt.split(line))
            for t in txt:
                txt_list.append({type: t})
            txt_list.append({type: r"<br>"})


for t in txt_list:
    print(t)
