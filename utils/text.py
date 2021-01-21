import re
import re
import jieba
from settings import stopwords_file, base_dir


# 过滤title
def filter_tilte(line):
    res = re.findall('(原标题|热门资讯|更多资讯|欢迎关注|请关注|节目|热线|微信|小编|编辑|日报|客户端")', line)
    return res is not None and len(res) > 0


# 函数, 过滤掉“\:：*？<>!！”, 路径不能包含相关字符，否则报错
def replace_exp(str):
    return re.sub(r'[:：*？?<>!！|\\"\\"]', '', str)


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


# 格式化多文本
def format_multi_article(sentences, stopwords=None):
    clean_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        # 如果一行少于等于8个字符就略过
        if len(sentence) <= 15 or filter_tilte(sentence):
            continue

        if stopwords is not None:
            sentence = clean_data(sentence, stopwords)
        else:
            # 分词切割
            sentence = " ".join(jieba.lcut(sentence))

        clean_sentences.append(sentence)

    return clean_sentences


# 简单字面计算相似度
def compute_sentence_pair_sim(sentence1, sentence2):
    set1 = set(jieba.lcut(sentence1))
    set2 = set(jieba.lcut(sentence2))
    inter_set = set1.intersection(set2)
    return len(inter_set) / min(len(set1), len(set2))