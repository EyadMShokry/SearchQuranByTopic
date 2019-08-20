# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 12:28:50 2019
@author: Esraa
"""
import numpy as np
from xlrd import open_workbook
import pandas as pd
from gensim.models import KeyedVectors
from nltk.tokenize import wordpunct_tokenize
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False


@app.route('/api/v1/resources/topics', methods=['GET'])
def topics():
    if 'query' in request.args:
        query = str(request.args['query'])
    else:
        return 'Error: No query field provided. Please specify all the required fields.'

    documents = []
    wb = pd.read_excel('TreeCode.xlsx')
    documents = [w['topic'] for i, w in wb.iterrows()]

    binary = True
    model_name = 'ksucca_full_cbow.bin'
    if binary:
        w2v_model = KeyedVectors.load_word2vec_format(model_name, binary=True)
    else:
        w2v_model = KeyedVectors.load(model_name)

    w2v_model.init_sims(replace=True)  # to save memory, can't continue learning!!
    vocab, vector_dim = w2v_model.syn0.shape
    embeddings = w2v_model
    dimension = vector_dim

    tokens = []

    try:
        try:
            txt = unicode(query, 'utf-8')  # py2
        except NameError:
            txt = query  # py3
        words = wordpunct_tokenize(txt)
        num = len(words)
    except TypeError:
        words, num = ['NA'], 0
    tokens.append(words)

    """ tokinize one topic"""

    """ get avarege of tokens vector"""
    for example in tokens:

        feature_vec = np.zeros((dimension,), dtype="float32")
        retrieved_words = 0
        for token in example:
            try:
                feature_vec = np.add(feature_vec, embeddings[token])
                retrieved_words += 1
            except KeyError:
                pass  # if a word is not in the embeddings' vocabulary discard it

        np.seterr(divide='ignore', invalid='ignore')
        feature_vec = np.divide(feature_vec, retrieved_words)

    queryVector = np.array([float(w) for w in feature_vec])
    """ get avarege of tokens vector"""

    '''data vectors'''
    data_vecrors = []
    data = pd.read_excel("TreeCode.xlsx")
    for index, row in data.iterrows():
        data_vecrors.append([float(w) for w in row["vector"].split(" ") if w != ""])

    """get top n queries simelar"""
    result = []
    to_sort_result = pd.DataFrame([], columns=["topic", "prob"])
    for i in range(0, len(documents)):
        #            print (i)
        result.append(
            embeddings.cosine_similarities(queryVector.reshape(300, ), np.array(data_vecrors[i]).reshape(1, 300))[0])
        to_sort_result.loc[i] = [documents[i], embeddings.cosine_similarities(queryVector.reshape(300, ),
                                                                              np.array(data_vecrors[i]).reshape(1,
                                                                                                                300))[
            0]]
    try:
        topicsNumber = 3
        result_ = [i for i in to_sort_result.nlargest(topicsNumber, "prob").iloc[:]['topic']]
        c = 1
        final_result = []
        for topic in result_:
            final_result.append(topic + "-" + str(c))
            c = c + 1

        print(final_result)
        return jsonify(AyaAndManual(final_result))

    except:
        return np.nan


@app.route('/api/v1/resources/topic', methods=['GET'])
def topic():
    if 'query' in request.args:
        query = str(request.args['query'])
    else:
        return 'Error: No query  field provided. Please specify all the required fields.'
    try:
        return jsonify(TopicList(query))
    except:
        return np.nan


def AyaAndManual(arr):
    SoraName = []
    VerseID = []
    ayaText = []
    Manual = []
    ChapterID = []
    PartID = []

    Aya_Manual_dic = {}
    wb = open_workbook('dataset_final.xlsx')
    values = []
    for s in wb.sheets():
        for row in range(s.nrows):
            col_value = []
            for col in range(s.ncols):
                value = (s.cell(row, col).value)
                try:
                    value = str(int(value))
                except:
                    pass
                col_value.append(value)
            values.append(col_value)
    del values[0]
    for aya in values:
        ChapterID.append(aya[0])
        PartID.append(aya[7])
        ayaText.append(aya[9])
        Manual.append(aya[4])
        SoraName.append(aya[8])
        VerseID.append(aya[2])

    topiccount = 1
    topic_Manual_dic = []
    for topic_rank in arr:
        Aya_Manual_dic = {}
        topic = topic_rank.split("-")[0]
        rank = topic_rank.split("-")[1]
        c = 0
        print(topic)

        print(rank)

        ayat = []
        if (topiccount == 1):
            topiccount = 0
            for manual in Manual:
                m = manual.split("-")
                for Topic in m:
                    Topic_More_Info = {}
                    if (topic == Topic):
                        Topic_More_Info["AyaText"] = ayaText[c]
                        Topic_More_Info["VerseNUM"] = VerseID[c]
                        Topic_More_Info["SoraName"] = SoraName[c]
                        Topic_More_Info["ChapterNUM"] = ChapterID[c]
                        Topic_More_Info["PartNUM"] = PartID[c]
                        ayat.append(Topic_More_Info)
                c = c + 1
        Aya_Manual_dic["Topic"] = topic
        Aya_Manual_dic["Ranking"] = rank
        Aya_Manual_dic["SubTopics"] = GetSubTopics(topic)
        Aya_Manual_dic["ayat"] = ayat
        topic_Manual_dic.append(Aya_Manual_dic)

        print(len(ayat))
    return topic_Manual_dic


################################################################################
def TopicList(t):
    SoraName = []
    VerseID = []
    ayaText = []
    Manual = []
    ChapterID = []
    PartID = []
    wb = open_workbook('dataset_final.xlsx')
    values = []
    for s in wb.sheets():
        for row in range(s.nrows):
            col_value = []
            for col in range(s.ncols):
                value = (s.cell(row, col).value)
                try:
                    value = str(int(value))
                except:
                    pass
                col_value.append(value)
            values.append(col_value)
    del values[0]
    for aya in values:
        ChapterID.append(aya[0])
        PartID.append(aya[7])
        ayaText.append(aya[9])
        Manual.append(aya[4])
        SoraName.append(aya[8])
        VerseID.append(aya[2])
    c = 0
    ayat = []
    BigDic = {}
    for manual in Manual:
        Topic_More_Info = {}
        if t in manual:
            Topic_More_Info["AyaText"] = ayaText[c]
            Topic_More_Info["VerseNUM"] = VerseID[c]
            Topic_More_Info["SoraName"] = SoraName[c]
            Topic_More_Info["ChapterNUM"] = ChapterID[c]
            Topic_More_Info["PartNUM"] = PartID[c]
            ayat.append(Topic_More_Info)
        c = c + 1;
    BigDic["SubTopics"] = GetSubTopics(t)
    BigDic["Ayat"] = ayat
    return BigDic


def GetSubTopics(input):
    df = pd.read_csv("TreeCode.csv", encoding='Windows-1256')
    topics = df.topic
    codes = df.code
    result = []
    for x in range(len(topics)):
        if (input == topics[x]):
            lis1 = codes[x].split('.')
            print(codes[x])
            for y in range(x, len(topics)):
                if (codes[x] in codes[y]):
                    lis2 = codes[y].split('.')
                    if (lis1[0] == lis2[0]):
                        if (lis2.__len__() - lis1.__len__() == 1):
                            result.append(topics[y])
    return result


app.run()
