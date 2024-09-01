# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import logging


class NovelPipeline:
    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        # 延迟到第一个 item 处理时再打开文件
        self.file = None

    def close_spider(self, spider):
        # 在爬虫结束时关闭文件
        if self.file:
            self.file.close()
            logging.info("Closed file after writing")

    def process_item(self, item, spider):
        if self.file is None:
            # 获取书名并去除 "目录"
            book_name = item['book_name'].replace("目录", "").strip()
            # 打开文件准备写入
            self.file = open(f"./{book_name}.txt", "w", encoding="utf-8")
            logging.info(f"Opened file '{book_name}.txt' for writing")

        title = item.get("title")
        text = item.get("text")

        # 确保标题和文本内容存在
        if title and text:
            title = f"### {title}"
            self.file.write(f"{title}\n{text}\n\n")
        else:
            logging.warning("Item 中缺少标题或文本内容，跳过该项。")

        return item
