import os


hot_url = "http://top.baidu.com/buzz?b=1&c=513"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"}
baidu_tieba_url = 'https://tieba.baidu.com/f/search/res?isnew=1&kw=&qw={}&un=&rn=10&pn={}&sd=&ed=&sm=2'
base_dir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
log_dir = os.path.join(base_dir, 'logs')
summary_dir = os.path.join(base_dir, 'summary')
stopwords_file = os.path.join(base_dir, 'stopwords.txt')
blog_url = "http://localhost/action/xmlrpc"
blog_username = "root"
blog_password = "hadoop"

# data_dir不存在就创建
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

# summary_dir不能存在就创建
if not os.path.exists(summary_dir):
    os.mkdir(summary_dir)

# 如果log_dir不存在就创建
if not os.path.exists(log_dir):
    os.mkdir(log_dir)