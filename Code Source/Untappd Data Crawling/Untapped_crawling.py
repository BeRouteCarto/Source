import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import psycopg2
import csv
import codecs

'''
#connect with the database
conn = psycopg2.connect(dbname="untapped", user="postgres",
        password="postgres", host="127.0.0.1", port="5432")
# 创建cursor以访问数据库
cur = conn.cursor()
cur.execute(
        'CREATE TABLE untapped_data ('
        'name   varchar(80),'
        'style varchar(100),'
        'url varchar(100)'
        ')'
    )
'''

def get_page(noun):
    base_url = 'https://untappd.com/search/more_search/venue?'
    params = {
        'offset': noun,
        'q': 'Munchen',
        'sort': 'all'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Host': 'untappd.com',
        'Cookie': '__cfduid=d4709b63fafba4b62e0d42db77e6200851542445421; untappd_user_v3_e=4e664e55c3229fe51380218d7c7a09eb548b303f908e08de4c7b89777a400bebf6e7f011f0ca919d14e986acceb6b00502e05408c62be4aee2987faf8b938963tayQl5rXR%2B%2BM39XZmaLqIWqI3U9s49BL1LCwp2qiaKR7%2FjYiSgdAAbCiv2C6HglDqKaCVJj6MxAYreFs6v%2BXtA%3D%3D; ut_tos_update=true; _ALGOLIA=cac6dbe6-3741-4e6a-a884-8a7023695216; __utma=13579763.1593236079.1542445426.1543403845.1543746870.4; __utmc=13579763; __utmz=13579763.1543746870.4.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
        'x-requested-with': 'XMLHttpRequest'
    }
    url = base_url + urlencode(params)
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def parse_one_page(html):
    result = list ()
    soup = BeautifulSoup(html, 'lxml')
    for div in soup.find_all(class_= 'beer-item'):
        contents = div.find_all(name = 'p')
        dict = {}
        dict["name"] = contents[0].a.string
        dict["style"] = contents[1].string
        dict["url"] = contents[0].a['href']
        #insert_query = "INSERT INTO untapped_data VALUES(%s,%s,%s)"
        data = [contents[0].a.string, contents[1].string, contents[0].a['href']]
        #cur.execute(insert_query, tuple(data))
        print(dict)
        result.append(data)
    return result

'''
def write_to_json(content):
    with open('result.txt','a') as f:
        f.write(json.dumps(content, ensure_ascii=False, ).encode('utf-8'))
'''

def main():
    max_page = 20
    csvfile = codecs.open('result.csv', 'w+', 'utf_8_sig')
    writer = csv.writer(csvfile)
    for page in range(1, max_page + 1):
        json = get_page(page*25)
        for i in parse_one_page(json):
            writer.writerow(i)
    csvfile.close()
    #conn.commit()
    #conn.close()
main()
