# 解析百度资讯搜索页
import requests
import traceback
import cchardet
from lxml import etree
from settings import baidu_news_url, headers
from gerapy_auto_extractor.extractors.list import extract_list
from gerapy_auto_extractor.extractors import extract_detail


# 抽取百度资讯url
def extract_news_urls(keyword):
    try:
        response = requests.get(url=baidu_news_url.format(keyword), headers=headers)
        detect_encoding = cchardet.detect(response.content)['encoding']
        response.encoding = detect_encoding
        content = response.text
        # 抽取资讯链接
        html = etree.HTML(content)
        links = html.xpath("//h3[contains(@class,'news-title')]")

        titles = []
        urls = []

        # 为每个链接抽取title和url
        for link in links:
            try:
                url = link.xpath('./a/@href')[0]
                title = ''.join(link.xpath('./a//text()'))
                print("title:{}\turl:{}".format(title, url))
                urls.append(url)
                titles.append(title)
            except:
                continue
    except:
        return None, None

    return titles, urls


# 抽取具体资讯页
def extract_news_detail(url):
    res = None
    try:
        response = requests.get(url=url, headers=headers)
        detect_encoding = cchardet.detect(response.content)['encoding']
        response.encoding = detect_encoding
        content = response.text
        res = extract_detail(content)
        # html = etree.HTML(content)
        # res = "\n".join(html.xpath("//p//text()"))
    except Exception as e:
        print(e)

    return res