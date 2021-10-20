#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File        :   utils.py
@Build_time  :   2021/09/24 16:11:52
@Author      :   東篱
@Version     :   1.0
@Descroption :   
'''

import random
import string


class Utils():
    def __init__(self):
        pass

    @staticmethod
    def clean_str(txt):
        """清除字符串中的无意义字符

        Args:
            txt (str): 需要处理的字符串

        Returns:
            str: 处理完的字符串
        """
        txt = txt.replace('\n', '').replace('\r', '')
        return txt.strip()

    @staticmethod
    def clean_list(list_):
        """清除列表中的无意义字符, 然后清除列表中的空元素

        Args:
            list_ (list): 需要处理的列表

        Returns:
            list: 处理完的列表
        """
        for i in range(len(list_)):
            list_[i] = Utils.clean_str(list_[i])
        # list_ = [x for x in list_ if x != '']
        list_ = list(filter(None, list_))
        return list_

    @staticmethod
    def clean_list_all(list_):
        for i in range(len(list_)):
            list_[i] = Utils.clean_str_all(list[i])
        list_ = list(filter(None, list_))
        return list_

    @staticmethod
    def startswithchinese(txt):
        if '\u4e00' <= txt[0] <= '\u9f5a':
            return True
        elif txt.startswith(tuple('0123456789')):
            return True
        else:
            return txt.startswith('（')

    @staticmethod
    def clean_str_with_stars(txt):
        return txt.replace('*', '')

    @staticmethod
    def clean_str_all(txt):
        return Utils.clean_str(Utils.clean_str_with_stars(txt))

    @staticmethod
    def gen_id(lenght:int):
        """生成注释id

        Returns:
            str: 注视id
        """
        return ''.join(random.sample(string.ascii_letters + string.digits, lenght))


if __name__ == '__main__':
    # txt = '\r\n test'
    # print(Utils.clean_str(txt))

    txt = '（二）承审员没有案子。湖南的司法制度，还是知事兼理司法，承审员助知事审案。知事及其僚佐要发财，全靠经手钱粮捐派，办兵差和在民刑诉讼上颠倒敲诈这几件事，尤以后一件为经常可靠的财源。几个月来，土豪劣绅倒了，没有了讼棍。农民的大小事，又一概在各级农会里处理。所以，县公署的承审员，简直没有事做。湘乡的承审员告诉我：“没有农民协会以前，县公署平均每日可收六十件民刑诉讼禀帖；有农会后，平均每日只有四五件了。”于是知事及其僚佐们的荷包，只好空着。'

    print(Utils.startswithchinese(txt))
