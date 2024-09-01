import scrapy
from ..items import NovelItem
import logging


class NovelSpider(scrapy.Spider):
    name = "novel"
    allowed_domains = ["69shuba.cx"]
    start_urls = ["https://69shuba.cx/book/46544/"]

    custom_settings = {
        'START_CHAPTER': None,  # 默认为 None，即从第一章开始
        'END_CHAPTER': None  # 默认为 None，即爬取到最后一章
    }

    def parse(self, response):
        # 提取书名
        book_name = response.xpath("//div[@class='catalog']/h1[@class='muluh1']/a/text()").extract_first().strip()
        logging.info(f"开始爬取《{book_name}》")

        # 存储书名以便在 Pipeline 中使用
        self.crawler.stats.set_value("book_name", book_name)

        # 提取章节列表中的所有链接
        chapter_links = response.xpath("//div[@class='catalog'][@id='catalog']//ul/li/a/@href").extract()

        # 颠倒章节链接的顺序
        chapter_links.reverse()

        # 获取起始章节和结束章节
        start_chapter = self.settings.get('START_CHAPTER')
        end_chapter = self.settings.get('END_CHAPTER')

        # 如果起始章节和结束章节都没有设置，则默认爬取所有章节
        start_chapter = int(start_chapter) if start_chapter else 1
        end_chapter = int(end_chapter) if end_chapter else len(chapter_links)

        # 爬取指定范围内的章节
        for index, link in enumerate(chapter_links[start_chapter - 1:end_chapter]):
            full_link = response.urljoin(link)
            # 设置优先级，使章节越靠前的优先被下载
            yield scrapy.Request(full_link, callback=self.parse_chapter, priority=-index, meta={'book_name': book_name})

    def parse_chapter(self, response):
        items = NovelItem()
        # 提取标题
        title = response.xpath("//h1[@class='hide720']/text()").extract_first().strip()

        # 检查标题是否以 "第" 开头并紧跟数字
        if not title.startswith("第") or not title[1:].lstrip("0123456789章"):
            return  # 如果标题不符合条件，跳过该链接

        items['title'] = title

        # 提取 <p> 标签中的文本内容
        p_content = response.xpath("//div[@id='txtright']/following-sibling::p/text()").extract()

        # 将 <p> 标签中的内容合并为一个字符串，每个段落之间用换行符分隔
        items['text'] = "\n".join([paragraph.strip() for paragraph in p_content])

        # 将书名也传递给 Pipeline
        items['book_name'] = response.meta['book_name']

        yield items
