# 解析百度资讯搜索页
import requests
import cchardet
from lxml import etree
from datetime import datetime
from utils.text import compute_sentence_pair_sim
from sklearn.metrics.pairwise import cosine_similarity
from settings import baidu_tieba_url, headers
from utils.text_bert import sentence_model
from utils.logger import logger


# 构造帖子url
def build_url(url):
    return "http://tieba.baidu.com{}".format(url)


# 抽取百度贴吧url
def extract_tieba_urls(keyword, page=1):
    res_urls, tiezi_titles = None, None
    try:
        logger.info("正在爬取贴吧:{}相关数据, page={}".format(keyword, page))
        response = requests.get(url=baidu_tieba_url.format(keyword, page), headers=headers)
        detect_encoding = cchardet.detect(response.content)['encoding']
        response.encoding = detect_encoding
        content = response.text
        # 抽取资讯链接
        html = etree.HTML(content)
        # 帖子item
        tiezi_items = html.xpath('//div[@class="s_post"]')

        tiezi_urls, tiezi_titles = [], []
        for tiezi_item in tiezi_items:
            item_url = tiezi_item.xpath('./span[@class="p_title"]/a/@href')
            item_title = tiezi_item.xpath('./span[@class="p_title"]/a//text()')
            date = tiezi_item.xpath('./font[contains(@class,"p_date")]/text()')

            if item_url is not None and item_title is not None and date is not None:
                item_url = "".join(item_url)
                item_title = "".join(item_title)
                # 获7天内帖子
                date = datetime.strptime(''.join(date), '%Y-%m-%d %H:%M')
                now = datetime.now()
                if (now - date).days > 15:
                    continue
                tiezi_urls.append(item_url)
                tiezi_titles.append(item_title.strip())

        res_urls = []
        res_titles = []
        # 通过keyword和文章title相似度超过0.5才通过
        for tiezi_url, tiezi_title in zip(tiezi_urls, tiezi_titles):
            sim = compute_sentence_pair_sim(keyword, tiezi_title)
            # 过滤相似度比较低的url
            if sim > 0.5:
                tiezi_url = build_url(tiezi_url)
                res_urls.append(tiezi_url)
                res_titles.append(tiezi_title)
    except Exception as e:
        logger.error(str(e))

    return res_urls, res_titles


# 抽取贴吧详情页
def extract_tieba_detail(url):
    res_list = []
    try:
        logger.info("正在爬取贴吧详情页url:{}".format(url))
        response = requests.get(url=url, headers=headers)
        detect_encoding = cchardet.detect(response.content)['encoding']
        response.encoding = detect_encoding
        content = response.text
        # res = extract_detail(content)
        html = etree.HTML(content)
        # 帖子相关数据
        tiezi_items = html.xpath('//div[contains(@id, "post_content")]')

        for tiezi_item in tiezi_items:
            tiezi_content = tiezi_item.xpath(".//text()")
            if tiezi_content is not None:
                tiezi_content = ''.join(tiezi_content)
                res_list.append(tiezi_content)

    except Exception as e:
        logger.error(str(e))

    return res_list