import re
import math


def load_file(fileName):
    data_set = {}
    vocabulary = {}
    with open(fileName, 'r', encoding='UTF-8')as file:
        for line in file:
            each_vocabulary = {}
            separate_line = line[:-1].split("：")
            separate_line[1] = separate_line[1].lower()
            separate_words = re.split(r'[.，,\s]', separate_line[1])
            for word in separate_words:
                if word != '':
                    if word not in vocabulary.keys():
                        vocabulary[word] = 0
                    vocabulary[word] += 1
            for word in separate_words:
                if word != '':
                    if word not in each_vocabulary:
                        each_vocabulary[word] = 0
                    each_vocabulary[word] += 1
            data_set[separate_line[0]] = each_vocabulary
    print(data_set)
    return data_set, vocabulary



def retrieve_by_boolean(data_set_doc, vocabulary, query):
    wiq=[]
    remaining_set=[]
    for word in vocabulary.keys():
        if word in query:
            wiq.append(1)
        else:
            wiq.append(0)
    for doc in data_set_doc:
        tag=1
        wij=retrieve_by_boolean_2(doc,vocabulary,data_set_doc)
        for i in range(len(wij)):
            if wij[i]-wiq[i]<0:
                tag=0
        if tag==1:
            remaining_set.append(doc)
    print("Boolean Model:",remaining_set)
    return remaining_set


def retrieve_by_boolean_2(doc, vocabulary,data_set_doc):
    wiq=[]
    for word in vocabulary.keys():
            if word in data_set_doc[doc].keys():
                wiq.append(1)
            else:
                wiq.append(0)
    return wiq

def find_ni(doc_set, vocabulary):
    ni_set = {}
    for word in vocabulary.keys():
        for doc in doc_set.keys():
            if word in doc_set[doc].keys():
                if word not in ni_set:
                    ni_set[word] = 0
                ni_set[word] += 1
    return ni_set


def find_sim(q, d, volcabulary, ni, N):
    wij = []
    wiq = []
    for word in volcabulary.keys():
        log2Nni = math.log(N / int(ni[word]), 2)
        if word not in d.keys():
            wij.append(0)
        else:
            log2fij = math.log(d[word], 2)
            wij.append((1 + log2fij) * log2Nni)
        if word not in q.keys():
            wiq.append(0)
        else:
            log2fiq = math.log(q[word], 2)
            wiq.append((1 + log2fiq) * log2Nni)
    numerator = 0
    temp1 = 0
    temp2 = 0
    for i in range(len(volcabulary)):
        numerator += wij[i] * wiq[i]
        temp1 += pow(wij[i], 2)
        temp2 += pow(wiq[i], 2)
    denominator = math.sqrt(temp1) * math.sqrt(temp2)
    sim=0
    if denominator !=0:
        sim = numerator / denominator
    return sim


def retrieve_by_vector(q, d_set, volcabulary, ni, N):
    sim_set = {}
    for doc in d_set:
        d = d_set[doc]
        sim = find_sim(q, d, volcabulary, ni, N)
        sim_set[doc] = sim
    h = sorted(sim_set.items(), reverse=True, key=lambda e: e[1])
    h1 = {}
    for i in h:
        h1[i[0]] = i[1]
    print("sort_sim:", h1)
    return h1



def get_content():
    relation = {}
    with open('document.txt', 'r', encoding='UTF-8')as file:
        for line in file:
            separate_line = line[:-1].split("：")
            relation[separate_line[0]]=separate_line[1]
    return relation

def get_voc_with_index(fileName,voc,ni):
    voc_index_map={}
    for word in voc.keys():
        voc_index_map[word]=[]
    with open(fileName, 'r', encoding='UTF-8')as file:
        for line in file:
            separate_line = line[:-1].split("：")
            separate_line[1] = separate_line[1].lower()
            separate_words = re.split(r'[.，,\s]', separate_line[1])
            for j in voc.keys():
                word_count = []
                i=0
                for word in separate_words:
                    i+=1
                    if word==j and j !='':
                        word_count.append(i)
                if len(word_count)!=0:
                    line = [separate_line[0], len(word_count), word_count]
                    voc_index_map[j].append(line)
    print(voc_index_map)
    return voc_index_map

def retrieve_by_invert(q,voc_index_map,data_set_doc):
    final_candidate_doc=set(data_set_doc.keys())
    for word in q:
        if word in voc_index_map.keys():
            candidate_doc=set()
            for i in range(len(voc_index_map[word])):
                candidate_doc.add(voc_index_map[word][i][0])
            final_candidate_doc=set(candidate_doc&final_candidate_doc)
    print(candidate_doc)
    return final_candidate_doc






# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    data_set_doc, vocabulary = load_file("document.txt")
    data_set_query, vocabulary_query = load_file("query.txt")
    print("voc",vocabulary)
    print(data_set_query,vocabulary_query)
    retrieve_by_boolean(data_set_doc,vocabulary, data_set_query['q1'])



    ni = find_ni(data_set_doc, vocabulary)
    retrieve_by_vector(data_set_query['q3'], data_set_doc, vocabulary, ni, len(data_set_doc))





    invert_index=get_voc_with_index("document.txt",vocabulary,ni)
    retrieve_by_invert(data_set_query['q2'], invert_index, data_set_doc)


