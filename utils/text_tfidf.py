import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.text import get_stopwords, format_multi_article
from settings import data_dir


# 计算句子和文本之间的相似度(tfidf方式)
def calculate_similarity_tfidf(sentence, doc):
    if doc == []: return 0
    vocab = {}
    for word in sentence.split():
        vocab[word] = 0

    doc_in_one_sentence = ''
    for t in doc:
        doc_in_one_sentence += (t + ' ')
        for word in t.split():
            vocab[word] = 0

    cv = TfidfVectorizer(vocabulary=vocab.keys())
    doc_vector = cv.fit_transform([doc_in_one_sentence])
    sentence_vector = cv.fit_transform([sentence])

    return cosine_similarity(doc_vector, sentence_vector)[0][0]


# 计算单篇文章中每个句子对于整篇文章的相似度
def calculate_each_sentence_similarity_tfidf(clean_sentences):
    scores = []
    # 用set去重
    clean_sentences_set = set(clean_sentences)
    for sentence in clean_sentences:
        # 去除本身句子之后的文章
        temp_doc = clean_sentences_set - set([sentence])
        score = calculate_similarity_tfidf(sentence, list(temp_doc))
        scores.append(score)

    return scores


# mmr tfidf 文本摘要
def mmr_summarization_tfidf(sentences, clean_sentences, scores, sim_ration=0.15, alpha=0.7):
    # 摘要选取的句子长度
    clean_summary = []
    summary = []

    while True:
        mmr = np.zeros(shape=len(sentences))
        index = 0

        for sentence, score in zip(sentences, scores):
            if not sentence in summary:
                # print(clean_summary)
                # print(calculate_similarity_tfidf(sentence, clean_summary))
                mmr[index] = alpha * score - (1 - alpha) * calculate_similarity_tfidf(sentence, clean_summary)
            index += 1
        selected = np.argmax(mmr)
        if mmr[selected] < sim_ration: break
        print("sentence:{}\tscore:{}".format(sentences[selected], mmr[selected]))
        clean_summary.append(clean_sentences[selected])
        summary.append(sentences[selected])

    return summary


if __name__ == '__main__':
    stopwords = get_stopwords()
    for file in os.listdir(data_dir):
        file = os.path.join(data_dir, file)
        with open(file, 'r', encoding='utf-8') as fr:
            sentences = fr.readlines()
            clean_sentences = format_multi_article(sentences, stopwords)
            scores = calculate_each_sentence_similarity_tfidf(clean_sentences)
            summary = mmr_summarization_tfidf(sentences, clean_sentences, scores)
            print("keyword:{}".format(file))
            print(summary)