import re
import re
import jieba
from settings import stopwords_file, base_dir


# 过滤title
def filter_tilte(line):
    res = re.findall('(原标题|热门资讯|更多资讯|欢迎关注|请关注|节目|热线|微信|小编")', line)
    return res is not None and len(res) > 0


# 函数, 过滤掉“\:：*？<>!！”, 路径不能包含相关字符，否则报错
def replace_exp(str):
    return re.sub(r'[\:：*？?<>!！|]', '', str)


# 获取停用词表
def get_stopwords():
    stopwords = set()
    with open(stopwords_file, 'r', encoding='utf-8') as fr:
        for word in fr.readlines():
            stopwords.add(word.strip())
    return stopwords


# 清洗数据
def clean_data(line, stopwords):
    word_list = jieba.lcut(line)
    word_list = [word for word in word_list if word not in stopwords]
    return " ".join(word_list)


# 读取单篇文章
def read_single_article(article_file, stopwords=None):
    sentences, clean_sentences = [], []
    with open(article_file, mode='r', encoding='utf-8') as fr:
        for line in fr.readlines():
            line = line.strip()

            # 如果一行少于等于8个字符就略过
            if len(line) <= 15 or filter_tilte(line):
                continue

            # 对一行用句号分割
            line_sentences = [sentence for sentence in line.split("。") if len(sentence) > 15]

            if stopwords is not None:
                clean_line_sentences = [clean_data(line_sentence, stopwords) for line_sentence in line_sentences]
                clean_sentences.extend(clean_line_sentences)

            sentences.extend(line_sentences)

    return sentences, clean_sentences