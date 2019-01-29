# -*- coding:utf-8 -*-
import flickrapi
#from flickr_api.api import flickr
import json
import psycopg2
from datetime import datetime
from datetime import timedelta
import sys
import importlib
import bboxList

importlib.reload(sys)

class flickrDataCollection:
    def __init__(self):
        bboxlist = bboxList.getbboxList()
        my_api_key = 'af8272040090608186dfb9e83bf95b61'
        my_secret = 'c2bed79585d24be3'
        self.flickr=flickrapi.FlickrAPI(my_api_key, my_secret,format='json')
        #auth = flickrapi.auth.AuthHandler()  # creates the AuthHandler object
        self.bbox = "11.3608, 48.0616, 11.7229, 48.2482"  # The leftbottom and upright cornor of area
        self.bboxlist = bboxlist.splitArea()
        #self.accuracy = 16  # street level
        self.content_type = 1  # photos only
        self.per_page = 250  # the number of data in each page
        #self.page = 500  # the maximum is 500
        self.start_date = "2010-10-01"  # start date
        self.end_date = "2011-10-01"  # end-date
        self.table = "flickr_data"

    def getPhotos(self, parameter):
        # print flickr.photos.geo.getLocation()
        geoPhotos = self.flickr.photos.search(bbox=parameter["bbox"],
                                         content_type=parameter["content_type"],
                                         per_page=parameter["per_page"],
                                         min_taken_date=parameter["min_taken_date"],
                                         max_taken_date=parameter["max_taken_date"])
        # test = xmltodict.parse(geoPhotos)
        # print test.values()
        # print geoPhotos
        id_list = []
        #geoPhotos = geoPhotos.lstrip(b"jsonFlickrApi(")
        #geoPhotos = geoPhotos.rstrip(b")")
        #print (geoPhotos)
        parsed_text = json.loads(geoPhotos)
        total_pages = int(parsed_text['photos']['pages'])
        print(total_pages)
        for page in range(1, total_pages + 1):
            all_Photos = self.flickr.photos.search(bbox=parameter["bbox"],
                                                  content_type=parameter["content_type"],
                                                  per_page=parameter["per_page"],
                                                  min_taken_date=parameter["min_taken_date"],
                                                  max_taken_date=parameter["max_taken_date"],page=page)
            json_photos = json.loads(all_Photos.decode('utf-8'))
        #print (type(parsed_text['photos']['photo']))
            for photo in json_photos['photos']['photo']:
                id_list.append(photo['id'])
                print("The photo %s is found." % photo['id'])
        return id_list

    # get the information and location of photos
    def getInfo(self, photoId):
        tag = []
        text = self.flickr.photos.getInfo(photo_id=photoId, format='json')
        #text = text.lstrip(b'jsonFlickrApi(')
        #text = text.rstrip(b')')
        parsed_data = json.loads(text)
        text_tag = parsed_data['photo']['tags']['tag']
        for line in text_tag:
            tag.append(line['_content'])
        longitude = parsed_data['photo']['location']['longitude']
        latitude = parsed_data['photo']['location']['latitude']
        time = parsed_data['photo']['dates']['taken']
        url_loc = parsed_data['photo']['urls']['url']
        url = url_loc[0]['_content']
        try:
            location = parsed_data['photo']['location']['locality']['_content']
        except Exception:
            location = []
        title = parsed_data['photo']['title']['_content']
        photo_id = parsed_data['photo']['id']
        info = {
            "photo_id": photo_id,
            "title": title,
            "tag": tag,
            "taken_time": time,
            "coordinates": (latitude, longitude),
            'location': location,
            'url': url
        }
        print("The information of photo %s is collected." % photo_id)
        return info

    def savetosql(self,data):
        global cur, conn
        try:
            conn = psycopg2.connect(dbname="flickr", user="postgres",password="postgres", host="127.0.0.1", port="5432")
            #db = MySQLdb.connect('host', 'user', 'password', 'database')
            cur = conn.cursor()
            print("connecting successfully")
        except psycopg2.Error as e:
            print("The error found in connnecting database%d: %s" % (e.args[0], e.args[1]))
        try:
            #cols = ', '.join(str(v) for v in data.keys())
            #print(type(data))
            #print(data)
            fields = [
                'photo_id',
                'title',
                'tag',
                'taken_time',
                'coordinates',
                'location',
                'url'
            ]
            my_data = [data[field] for field in fields]
            insert_query = "INSERT INTO flickr_data VALUES(%s,%s,%s,%s,%s,%s,%s)"
            #values = '"' + '","'.join(str(v) for v in data.values()) + '"'
            #sql = "INSERT INTO %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s=%s" % (
            #table, cols, values, 'photo_id', 'photo_id')  # the primary key is photo_id
            #print (sql)
            try:
                result = cur.execute(insert_query,tuple(my_data))
                conn.commit()
                conn.close()
                # Check the result of command execution
                if result:
                    print("This data is imported into database.")
                else:
                    return 0
            except psycopg2.Error as e:
                # rollback if error
                conn.rollback()
                # duplicate primary key
                if "key 'PRIMARY'" in e.args[1]:
                    print("Data Existed")
                else:
                    print("Insertion faied, reason is %d: %s" % (e.args[0], e.args[1]))
        except psycopg2.Error as e:
            print("Error found in database, reason is %d: %s" % (e.args[0], e.args[1]))

    def main(self):
        format_time = "%Y-%m-%d"
        # auth.set_verifier = '72157671561687371-cbb80beb464db307'
        # flickr_api.set_auth_handler(auth)
        # perms = "read" # set the required permissions
        # url = auth.get_authorization_url(perms)
        # print url
        # print flickr.reflection.getMethodInfo(method_name = "flickr.photos.search")
        difftime = datetime.strptime(self.end_date, format_time) - datetime.strptime(self.start_date, format_time)
        intervals = int(difftime.days / 365)  # the difference by years
        year = timedelta(days=365)
        for i in range(0, intervals):
            min_taken_date = str(datetime.strptime(self.start_date, format_time) + year * i)
            max_taken_date = str(datetime.strptime(self.start_date, format_time) + year * (i + 1))
            print ("Collection start time is " + min_taken_date + "Collection end time is " + max_taken_date)
            area_code = 50
            for area in self.bboxlist[48:80]:
                print("Area " + str(area_code) + " is being searched now.")
                bboxpara = ','.join(str(v) for v in area)
                print(bboxpara)
                parameter = {"bbox": bboxpara,
                             "content_type": self.content_type,
                             "per_page": self.per_page,
                             "min_taken_date": min_taken_date,
                             "max_taken_date": max_taken_date
                             }
                photoIDs = self.getPhotos(parameter)
                try:
                    for photoID in photoIDs:
                        photoInfo = self.getInfo(photoID)
                        #print(photoID)
                        #  print (photoInfo)
                        self.savetosql(photoInfo)
                except Exception:
                    print("photo: " + str(photoID) + " is not acquired.")
                area_code += 1


flickr_downloader = flickrDataCollection()
flickr_downloader.main()
# print flickr_downloader.getInfo('23536223114')