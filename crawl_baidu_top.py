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
    # 贴吧帖子urls
    tiezi_urls = []
    for page in range(1,4):
        tmp_urls = extract_news_urls(keyword, page)
        if tmp_urls is not None:
            tiezi_urls += tmp_urls
        # 随机休眠，避免被禁止爬取工作
        time.sleep(random.randint(3, 10))

    if len(tiezi_urls) > 0:
        res_list = []

        # 遍历爬取url
        for url in tiezi_urls:
            tmp_list = extract_news_detail(url)
            if tmp_list is not None and len(tmp_list) > 0:
                res_list += tmp_list
                print(tmp_list)
            time.sleep(random.randint(3, 10))

        # 保存数据
        print("keyword:{}保存数据".format(keyword))
        save_data(keyword, res_list)


# 保存数据
def save_data(keyword, res_list):
    # 根据关键词创建对应目录
    save_dir = os.path.join(data_dir)
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    write_res_list = []
    for res in res_list:
        res = res.strip()
        line_list = [line.strip() for line in res.split("。")]
        write_res_list += line_list

    # 保存文件路径
    save_file = os.path.join(save_dir, '{}.txt'.format(replace_exp(keyword)))

    # 保存数据
    with open(save_file, mode='a', encoding='utf-8') as fw:
        for line in write_res_list:
            if len(line) < 5: continue
            line = line.replace('\r', '').replace('\n', '')
            fw.write(line + "\n")


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