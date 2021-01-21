# 爬取百度实时热点
import random
import time
import os
import requests
import cchardet
from pybloom_live import ScalableBloomFilter
from lxml import etree
from settings import hot_url, headers
from spider_detail import extract_tieba_urls, extract_tieba_detail
from summarization import multi_document_summarization
from text_cluster import text_cluster
from utils.logger import logger
from utils.TypechoUtils import TypechoUtils
from settings import data_dir
from utils.text import replace_exp


# 获取百度热门关键词
def get_hot_keywords():
    count = 5
    keywords = None
    # 最多5次循环获取数据
    while count > 0:
        try:
            logger.info("爬取百度热门关键词")
            response = requests.get(url=hot_url, headers=headers)
            # 获取encoding
            detect_encoding = cchardet.detect(response.content)['encoding']
            response.encoding = detect_encoding
            html = response.text

            root = etree.HTML(html)
            keywords = [replace_exp(str(item)) for item in root.xpath("//table[@class='list-table']//a[@class='list-title']/text()")]
            time.sleep(random.randint(3, 10))
            return keywords
        except Exception as e:
            logger.error(str(e))
            count -= 1
            continue

    return keywords


# 根据热门关键词爬取相关信息
def crawl_by_keyword_tieba(keyword):
    # 抽取标题和链接
    logger.info("开始keyword:{}爬虫贴吧工作".format(keyword))
    # 贴吧帖子urls
    tiezi_urls, tiezi_titles = [], []
    for page in range(1,6):
        tmp_urls, tmp_titles = extract_tieba_urls(keyword, page)
        if tmp_urls is not None and tmp_titles is not None:
            tiezi_urls += tmp_urls
            tiezi_titles += tmp_titles
        # 随机休眠，避免被禁止爬取工作
        time.sleep(random.randint(3, 10))

    # 判断url和title个数是否相等
    assert len(tiezi_titles) == len(tiezi_urls), "len(tiezi_titles) != len(tiezi_urls)"

    res_list = []

    if len(tiezi_urls) > 0 and len(tiezi_titles) > 0:
        # 遍历爬取url
        for url, title in zip(tiezi_urls, tiezi_titles):
            tmp_list = extract_tieba_detail(url)
            if tmp_list is not None and len(tmp_list) > 0:
                res_list.append((title, tmp_list))
                logger.info("贴吧:title:{}\tsentences:{}\n".format(url, tmp_list))
            time.sleep(random.randint(3, 10))

    # 保存文件
    save_data(keyword, res_list)

    return res_list


# 保存数据到文件
def save_data(keyword, res_list):
    dir_name = os.path.join(data_dir, keyword)
    if not os.path.exists(dir_name) and len(res_list) > 0:
        os.mkdir(dir_name)
    # 依次保存
    for title, sentences in res_list:
        title = replace_exp(title)
        with open(os.path.join(dir_name, '{}.txt'.format(title)), 'w', encoding='utf-8') as fw:
            for sentence in sentences:
                fw.write(sentence.strip() + "\n")
        logger.info("保存{}.txt成功".format(title))


# 爬虫主函数
def crawl():
    # 博客发布工具
    utils = TypechoUtils()
    # bloomfilter过滤关键词
    bloom_filter = ScalableBloomFilter(initial_capacity=100, error_rate=0.001, mode=ScalableBloomFilter.LARGE_SET_GROWTH)
    # 获取热门关键词
    keywords = get_hot_keywords()

    # keywords 有数据
    if keywords is not None:
        # 遍历热门关键词
        for keyword in keywords:
            # 如果已经爬虫过略过
            if keyword in bloom_filter: continue

            # 添加关键词
            bloom_filter.add(keyword)

            sentences = crawl_by_keyword_tieba(keyword)
            # # 多文本摘要
            # summary_list = multi_document_summarization(keyword, sentences)
            # if len(summary_list) > 5:
            #     cluster_topic = text_cluster(summary_list)
            #     print("keyword:{}".format(keyword))
            #
            #     contents = []
            #     for k, topic_content_list in cluster_topic.items():
            #         for topic_content in topic_content_list:
            #             contents.append(topic_content)
            #             print("topic:{}\tcontent:{}".format(k, topic_content))
            #     logger.info("发布博客文章, title:{}".format(keyword))
            #     utils.add_article(title=keyword, sentences=contents)


if __name__ == '__main__':
    crawl()