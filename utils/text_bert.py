import os
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils.text import get_stopwords


# 加载sentence bert模型
sentence_model = SentenceTransformer('paraphrase-distilroberta-base-v1')


# 计算句子和文本之间的相似度(bert)
def calculate_similarity_bert(sentence_vectors, index, summary_idx):
    if summary_idx == []: return 0
    sim_list = cosine_similarity(sentence_vectors[index].reshape(1,-1), sentence_vectors[summary_idx])[0]
    return np.mean(sim_list)


# 计算单篇文章中每个句子对于整篇文章的相似度
def calculate_each_sentence_similarity_bert(title_vector, sentence_vectors):
    scores = []
    for index, sentence_vector in enumerate(sentence_vectors):
        sim_list = cosine_similarity(sentence_vector.reshape(1,-1), sentence_vectors)[0]
        scores.append(np.mean(sim_list))

    scores_title = cosine_similarity(title_vector.reshape(1, -1), sentence_vectors)[0]
    scores = [score1 + score2 for score1, score2 in zip(scores, scores_title)]

    max_score, min_score = max(scores), min(scores)
    scores = [(score - min_score) / (max_score - min_score) for score in scores]
    return scores


def mmr_summarization_bert(sentences, sentence_vectors, scores, title_vector, sim_ratio=0.10, alpha=0.7):
    # 摘要选取的句子长度
    summary, summary_idx = [sentences[np.argmax(scores)]], [np.argmax(scores)]

    while True:
        mmr = np.zeros(shape=len(sentences))
        index = 0

        for sentence, score in zip(sentences, scores):
            if not sentence in summary:
                # print(clean_summary)
                # print(calculate_similarity_tfidf(sentence, clean_summary))
                score_title = cosine_similarity(title_vector.reshape(1, -1), sentence_vectors[index].reshape(1,-1))[0]
                mmr[index] = alpha * (score * 0.3 + score_title * 0.7) - (1 - alpha) * calculate_similarity_bert(sentence_vectors, index, summary_idx)
            index += 1

        selected = np.argmax(mmr)
        if mmr[selected] < sim_ratio:
            break

        # print("sentence:{}\tscore:{}".format(sentences[selected], mmr[selected]))
        summary.append(sentences[selected])
        summary_idx.append(selected)

    return summary, summary_idx


if __name__ == '__main__':
    pass
    # stopwords = get_stopwords()
    # sentences, clean_sentences = [], []
    # title = ""
    # for file in os.listdir("G:/code/python/mashup/data/不建议同时接种新冠疫苗和HPV疫苗"):
    #     single_sentences, single_clean_sentences = read_single_article(
    #         os.path.join("G:/code/python/mashup/data/不建议同时接种新冠疫苗和HPV疫苗", file), stopwords)
    #     sentences += single_sentences
    #     clean_sentences += single_clean_sentences
    #     file_list = re.split("[-_-|]",file)
    #     file = file_list[0] if len(file_list) > 0 else file
    #
    # # 对句子去重
    # sentences = list(set(sentences))
    # # 标题
    # title_vector = sentence_model.encode(title)
    # # 将所有语句转换成向量
    # sentence_vectors = sentence_model.encode(sentences)
    #
    # if len(sentences) > 15:
    #     scores = calculate_each_sentence_similarity_bert(title_vector, sentence_vectors)
    #     print(scores)
    #     summary = mmr_summarization_bert(sentences, sentence_vectors, scores, title_vector)
    #     for sentence in summary:
    #         print(sentence)