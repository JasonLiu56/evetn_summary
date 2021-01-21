# 针对提取的数据进行聚类
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from settings import summary_dir
from utils.text_bert import sentence_model
from utils.logger import logger


def get_max_similarity(dict_topic, vector):
    max_value = 0
    max_index = -1
    for k, cluster in dict_topic.items():
        one_similarity = np.mean([cosine_similarity(vector.reshape(1,-1), v.reshape(1,-1))[0][0] for v in cluster])
        if one_similarity > max_value:
            max_value = one_similarity
            max_index = k

    return max_index, max_value


# 文本聚类
def text_cluster(texts, theta=0.85):
    # 将文本转成向量集
    text_vectors = sentence_model.encode(texts)

    # 字典topic
    dict_topic = {}
    cluster_topic = {}
    num_topic = 0

    logger.info("正在进行文本聚类工作")

    for vector, text in zip(text_vectors, texts):
        if num_topic == 0:
            dict_topic[num_topic] = []
            dict_topic[num_topic].append(vector)
            cluster_topic[num_topic] = []
            cluster_topic[num_topic].append(text)
            num_topic += 1
        else:
            max_index, max_value = get_max_similarity(dict_topic, vector)
            # 将给定语句分配到现有的，最相似的主题中
            if max_value >= theta:
                dict_topic[max_index].append(vector)
                cluster_topic[max_index].append(text)
            else:
                dict_topic[num_topic] = []
                dict_topic[num_topic].append(vector)
                cluster_topic[num_topic] = []
                cluster_topic[num_topic].append(text)
                num_topic += 1

    return cluster_topic


if __name__ == '__main__':
    for index, file in enumerate(os.listdir(summary_dir)):
        file = os.path.join(summary_dir, file)
        print("index:{}\tfile:{}".format(index, file))
        with open(file, 'r', encoding='utf-8') as fr:
            lines =[line.strip() for line in fr.readlines() if len(line.strip()) > 0]
            _, cluster_topic = text_cluster(texts=lines, theta=0.85)
            for k, topic_content_list in cluster_topic.items():
                for topic_content in topic_content_list:
                    print("topic:{}\tcontent:{}".format(k, topic_content))
        print("------------------------------------------------------------")