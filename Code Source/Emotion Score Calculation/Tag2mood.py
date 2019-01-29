import json
import pandas as pd
import nltk
import psycopg2
#corpus_root=r'D:\Mapping project\Corpus'
#wordlists=PlaintextCorpusReader(corpus_root,'.*')
#wordlists.fileids()
#"tag": ["munich", "germany", "railroad"]
#load_dict[i]["properties"]["tag"]
with open("point.json",'r',encoding='UTF-8') as load_f:
    load_dict = json.load(load_f)


#generate a trainer list(valence, arousal)
# combining the German and English corporal
data_german = pd.read_table("D:/Mapping project/Corpus/ratings_lrec16_koeper_ssiw.txt",header=0,index_col=None,
                           encoding="utf-8")
data_english = pd.read_csv("D:/Mapping project/Corpus/Ratings_Warriner_et_al.csv",header=0,index_col=0,
                           encoding="utf-8")
word_list = ([row['Word'] for index,row in data_german.iterrows()]+
             [row['Word'] for index,row in data_english.iterrows()])
Dict = ([(row['Word'],row['Val'],row['Arou']) for index,row in data_german.iterrows()]+
       [(row['Word'],row['V.Mean.Sum'],row['A.Mean.Sum']) for index,row in data_english.iterrows()])

#classify the word and calculate the score in valence&Arousal(V1+V2+..+Vn)/n (Vn!=NA)
testlist=["munich", "germany", "railroad"]
def coordinate(Dict,testlist):
    score_val = 0
    score_arou = 0
    time = 0
    for word in testlist:
        if word in word_list:
            print(word)
            pos = word_list.index(word)
            score_val = score_val + Dict[pos][1]
            score_arou = score_arou + Dict[pos][2]
            time = time + 1
    if time > 0:
        final_val = score_val / time - 5
        final_arou = score_arou / time - 5
    else:
        final_arou = 0
        final_val = 0
    return (final_val,final_arou)

#calculate the final score and divide into different category
#emtion category: Pleasure, Distress,Depression,Contenment
#according to the coordinate of (V,A)
def emotion_define (coordinate):
    emotion = 0
    if coordinate[0]>0 and coordinate[1]>0:
        emotion = 1
    if coordinate[0]<0 and coordinate[1]>0:
        emotion = 2
    if coordinate[0]<0 and coordinate[1]<0:
        emotion = 3
    if coordinate[0]>0 and coordinate[1]<0:
        emotion = 4
    if coordinate[0]==0 and coordinate[1]==0:
        emotion = 5
    return emotion

for element in load_dict:
    tag = element["properties"]["tag"]
    coor = coordinate(Dict,tag)
    emo = emotion_define(coor)
    element["properties"]["emotion"] = emo
#save the result into .json file
file = open('point_emotion.json','w',encoding='utf-8')
file.write(json.dumps(load_dict,ensure_ascii=False))
file.close()