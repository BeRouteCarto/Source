#-*- coding: utf-8 -*-
import psycopg2

# 连接数据库
conn = psycopg2.connect(dbname="flickr", user="postgres",
        password="postgres", host="127.0.0.1", port="5432")

# 创建cursor以访问数据库
cur = conn.cursor()
cur.execute(
        'CREATE TABLE flickr_data ('
        'photo_id    int8,'
        'title varchar(80),'
        'tag   text[],'
        'taken_time   timestamp,'
         'coordinates point,'
        'location text,'
         'url varchar(100)'
        ')'
    )
#cols='photo_id', 'title', 'tag', 'taken_time', 'coordinates', 'location', 'url'
values="5801567182","20110605-032","['allianzarena','münchen','bayern','deutschland','deu']","2011-06-05 12:55:59","('11.625058','48.219855')","[]","https://www.flickr.com/photos/wildsau/5801567182/"
list= values[2].split(',')
sql = "INSERT INTO %s(tag)VALUES %s " %('flickr_data', list)
#sql = "INSERT INTO %s(location) VALUES %s" %('flickr_data', values[5])
cur.execute(sql)
conn.commit()
conn.close()