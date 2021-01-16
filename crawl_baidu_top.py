# 爬取百度实时热点
import os
import random
import time
import requests
import cchardet
from lxml import etree
from settings import hot_url, headers, data_dir
from utils.text import replace_exp
from spider_detail import extract_news_urls, extract_news_detail


# 获取百度热门关键词
def get_hot_keywords():
    count = 5
    keywords = None
    # 最多5次循环获取数据
    while count > 0:
        try:
            print("爬取百度热门关键词")
            response = requests.get(url=hot_url, headers=headers)
            # 获取encoding
            detect_encoding = cchardet.detect(response.content)['encoding']
            response.encoding = detect_encoding
            html = response.text

            root = etree.HTML(html)
            keywords = root.xpath("//table[@class='list-table']//a[@class='list-title']/text()")
            time.sleep(random.randint(3, 10))
            return keywords
        except Exception as e:
            print(e)
            count -= 1
            continue

    return keywords


# 根据热门关键词爬取相关信息
def crawl_by_keyword(keyword):
    # 抽取标题和链接
    print("开始keyword:{}爬虫工作".format(keyword))
    titles, urls = extract_news_urls(keyword)
    # 随机休眠，避免被禁止爬取工作
    time.sleep(random.randint(3, 10))

    if titles is not None and urls is not None:
        res_list = []

        # 遍历爬取url
        for url in urls:
            res = extract_news_detail(url)
            print(res)
            # 有数据则添加
            if res is not None:
                res_list.append(res)
            time.sleep(random.randint(3, 10))

        # 保存数据
        print("keyword:{}保存数据".format(keyword))
        save_data(keyword, titles, res_list)


# 保存数据
def save_data(keyword, titles, res_list):
    # 根据关键词创建对应目录
    save_dir = os.path.join(data_dir, replace_exp(keyword))
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    # 遍历 titles, res_list
    for title, res in zip(titles, res_list):
        save_file = os.path.join(save_dir, '{}.txt'.format(replace_exp(title)))
        # 如果res['content']为None不保存 或者res['content']长度太短
        if res['content'] is None or len(res['content']) < 10:
            continue

        # 保存数据
        with open(save_file, mode='a', encoding='utf-8') as fw:
            fw.write(res['content'] + "\n")


# 爬虫主函数
def crawl():
    # 获取热门关键词
    keywords = get_hot_keywords()

    # keywords 有数据
    if keywords is not None:
        # 遍历热门关键词
        for keyword in keywords:
            crawl_by_keyword(keyword)


if __name__ == '__main__':
    crawl()