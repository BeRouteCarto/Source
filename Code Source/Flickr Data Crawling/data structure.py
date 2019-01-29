#import numpy as np
#values="5801567182","20110605-032","['allianzarena','münchen','bayern','deutschland','deu']","2011-06-05 12:55:59","('11.625058','48.219855')","[]","https://www.flickr.com/photos/wildsau/5801567182/"
#values=values[2].lstrip('[')
#values=values[2].rstrip(']')
#print(values)
#point=values[4].split(',')
#array=numpy.array(list)
#list = np.array(list)
#print (type(list))
#n=len(lists)
#for list in lists:
#list_values = '"' + '","'.join(list for list in lists)+ '"'
#print (list_values)
#print (type(arr))
#print(point)

#-*- coding: utf-8 -*-
import psycopg2
import json
my_data={'photo_id': '5801567182', 'title': '20110605-032', 'tag': ['allianzarena', 'münchen', 'bayern', 'deutschland', 'deu'], 'taken_time': '2011-06-05 12:55:59', 'coordinates': ('11.625058', '48.219855'), 'location': [], 'url': 'https://www.flickr.com/photos/wildsau/5801567182/'}
print(type(my_data))
#my_data=json.dumps(data)
#print(type(my_data))
# 连接数据库
conn = psycopg2.connect(dbname="flickr", user="postgres",
        password="postgres", host="127.0.0.1", port="5432")
table = "flickr_data"
# 创建cursor以访问数据库
cur = conn.cursor()
cur.execute(
        'CREATE TABLE flickr_data ('
        'photo_id    int8,'
        'title varchar(80),'
        'tag   text[],'
        'taken_time   timestamp,'
         'coordinates text,'
        'location text,'
         'url varchar(100)'
        ')'
    )
fields = [
    'photo_id',
    'title',
    'tag',
    'taken_time',
    'coordinates',
    'location',
    'url'
]

my_data = [my_data[field] for field in fields]
#print(my_data)
#values=["5801567182","20110605-032","['allianzarena','münchen','bayern','deutschland','deu']","2011-06-05 12:55:59","('11.625058','48.219855')","[]","https://www.flickr.com/photos/wildsau/5801567182/"]
#print(tuple(values))
# need a placeholder (%s) for each variable
# refer to postgres docs on INSERT statement on how to specify order
#cur.execute("INSERT INTO test VALUES (%s,%s,%s,%s,%s,%s,%s)"%tuple(my_data))
#cur.execute("CREATE TABLE test (data json);")
insert_query = "INSERT INTO flickr_data VALUES(%s,%s,%s,%s,%s,%s,%s)"
cur.execute(insert_query,tuple(my_data))
#cur.execute("""INSERT INTO test VALUES (1,my_data)""")
#sql = "INSERT INTO test VALUES(1,data)"
#sql = tsql.format(json=data)
#print(sql)
#cur.execute(sql)
conn.commit()
conn.close()
