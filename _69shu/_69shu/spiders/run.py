# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : run.py
# @Author: Jox
# @Time  : 2024/09/01
# @Desc  :

from scrapy import cmdline

if __name__ == '__main__':
    # cmdline.execute('scrapy crawl novel --nolog'.split())
    cmdline.execute('scrapy crawl novel -s START_CHAPTER=456 -s END_CHAPTER=457 -L ERROR'.split())