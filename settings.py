import os


hot_url = "http://top.baidu.com/buzz?b=1&c=513"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"}
baidu_news_url = 'http://www.baidu.com/s?&tn=news&ie=utf-8&word={}'
base_dir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
stopwords_file = os.path.join(base_dir, 'stopwords.txt')

# data_dir不存在就创建
if not os.path.exists(data_dir):
    os.mkdir(data_dir)