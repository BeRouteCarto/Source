import json
import pandas as pd
import csv
import numpy

with open("point_new.json",'r',encoding='UTF-8') as load_f:
    load_dict = json.load(load_f)

data_german = pd.read_table("D:/Mapping project/Corpus/ratings_lrec16_koeper_ssiw.txt",header=0,index_col=None,
                           encoding="utf-8")
data_english = pd.read_csv("D:/Mapping project/Corpus/Ratings_Warriner_et_al.csv",header=0,index_col=0,
                           encoding="utf-8")
word_list = ([row['Word'] for index,row in data_german.iterrows()]+
             [row['Word'] for index,row in data_english.iterrows()])
Dict = ([(row['Word'],row['Val'],row['Arou']) for index,row in data_german.iterrows()]+
       [(row['Word'],row['V.Mean.Sum'],row['A.Mean.Sum']) for index,row in data_english.iterrows()])


def emo_coordinate(Dict,testlist):
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
        final_val = score_val / time
        final_arou = score_arou / time
    else:
        final_arou = 0
        final_val = 0
    return (final_val,final_arou)

fileHeader = ["ID","longitude","latitude","valence","arousal","emo_dis"]
csvFile = open("point_emo.csv", "w")
writer = csv.writer(csvFile)
writer.writerow(fileHeader)

#write into .csv file
for element in load_dict:
    if element["properties"]["polygone_id"] > 0 :
        tag = element["properties"]["tag"]
        coor = emo_coordinate(Dict, tag)
        element["properties"]["emo_coords"] = coor
        distance = numpy.sqrt(numpy.square(coor[0])+numpy.square(coor[1]))
        longitude = element["geometry"]["coordinates"][0]
        latitude = element["geometry"]["coordinates"][1]
        data = [element["properties"]["ID"],longitude,latitude,coor[0],coor[1],distance]
        writer.writerow(data)

csvFile.close()
