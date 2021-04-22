import numpy as np
import re
from nltk.corpus import stopwords
import pandas as pd
import scipy
import openpyxl as oxl
import sys
import language_translator as lt

incorrectAnnouncement = sys.argv[1]
translator_code = sys.argv[2]
#D:/MTCode_V31/

#Reading excel file to append data
announcementFilePath = "D:/MTCode_V31/announcement_list.xlsx"
wb = oxl.load_workbook(announcementFilePath)
sheet = wb.active
append= False

gloveFile = "D:/MTCode_V31/glovedata/glove.6B.50d.txt"
announcementFile = pd.read_excel(announcementFilePath)
originalText = announcementFile['originalscript']


def loadGloveModel(gloveFile):
    # print('Loading Glove Model')
    with open(gloveFile, encoding='utf8')as f:
        content = f.readlines()
    model={}
    for eachline in content:
        splitLine = eachline.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    # print("Done", len(model), 'words loaded!')
    return model


def preprocess(raw_text):
    # keep only words
    letters_only_text = re.sub("[^a-zA-Z]", " ", raw_text)
    # convert words to lower case and split
    words = letters_only_text.lower().split()
    # removing stopwords
    stopword_set = set(stopwords.words('english'))
    clean_words = list(set([w for w in words if w not in stopword_set]))

    return clean_words

def cosine_distance_wordembedding_method(s1, s2):
    vector_1 = np.mean([model[word] for word in preprocess(s1)],axis=0)
    vector_2 = np.mean([model[word] for word in preprocess(s2)], axis=0)
    cosine = scipy.spatial.distance.cosine(vector_1, vector_2)
    # print('WEM with cosine distance and sentences are similar to:',
    #       round((1-cosine)*100,2),'%')
    return round((1-cosine)*100,2)

model = loadGloveModel(gloveFile)

similarity_value = {}
max_similarity_value = 0
for announcement in originalText:
    similarity = cosine_distance_wordembedding_method(announcement, incorrectAnnouncement)
    similarity_value[similarity]=announcement
    #print(similarity, max(similarity_value))
    print('"'+announcement+'"has similarity of '+str(similarity)+" %")

if (bool(similarity_value)):
    max_similarity_value = max(similarity_value)
    matched_data = similarity_value[max_similarity_value]
    translated_text = lt.translator(matched_data,translator_code)
    universal_data2 = lt.universal('"'+matched_data+'"'+"++ "+translated_text+"++ "+"has highest similarity of "+str(max(similarity_value))+"%")
    print(universal_data2)
    # print(announcement, similarity)
    sys.stdout.flush()
    append = False
else:
    append=True

if append == True:
    sheet.append([incorrectAnnouncement])
    wb.save(announcementFilePath)




