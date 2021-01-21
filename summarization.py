import os
from utils.text_bert import sentence_model, calculate_each_sentence_similarity_bert, mmr_summarization_bert
from utils.logger import logger


# 获取多文本关键信息
def multi_document_summarization(title, sentences):
    # 对句子去重
    sentences = list(set(sentences))
    # 标题
    title_vector = sentence_model.encode(title)
    # 将所有语句转换成向量
    sentence_vectors = sentence_model.encode(sentences)

    if len(sentences) > 5:
        logger.info("正在处理多文本摘要处理工作")
        scores = calculate_each_sentence_similarity_bert(title_vector, sentence_vectors)
        summary, summary_idx = mmr_summarization_bert(sentences, sentence_vectors, scores, title_vector)
        return summary

    return []


if __name__ == '__main__':
    for file in os.listdir("G:\\code\\python\\event_summary\\data"):
        path = os.path.join("G:\\code\\python\\event_summary\\data", file)
        multi_document_summarization(path)