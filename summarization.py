import os
import re
from utils.text import read_single_article
from utils.text_bert import sentence_model, calculate_each_sentence_similarity_bert, mmr_summarization_bert


# 获取多文本关键信息
def multi_document_summarization(path):
    sentences, clean_sentences = [], []
    title = ""
    for file in os.listdir(path):
        single_sentences, single_clean_sentences = read_single_article(
            os.path.join(path, file))
        sentences += single_sentences
        clean_sentences += single_clean_sentences
        file_list = re.split("[-_-|]",file)
        title += file_list[0] if len(file_list) > 0 else file

    # 对句子去重
    sentences = list(set(sentences))
    # 标题
    title_vector = sentence_model.encode(title)
    # 将所有语句转换成向量
    sentence_vectors = sentence_model.encode(sentences)

    if len(sentences) > 15:
        scores = calculate_each_sentence_similarity_bert(title_vector, sentence_vectors)
        summary = mmr_summarization_bert(sentences, sentence_vectors, scores, title_vector)

        # 保存文件
        if len(summary) > 15:
            filename = os.path.join("./summary", path.split("\\")[-1])
            with open(filename, 'w', encoding="utf-8") as fw:
                for sentence in summary:
                    fw.write(sentence + "\n")

            print("保存:{}".format(filename))


if __name__ == '__main__':
    for file in os.listdir("E:\\code\\python\\mashup\\data"):
        path = os.path.join("E:\\code\\python\\mashup\\data", file)
        multi_document_summarization(path)