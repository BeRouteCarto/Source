from urllib.parse import urlencode
import urllib.request
import urllib
import json


base_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'

key= 'AIzaSyCfo205SFACBi4hjhWPdTzg1ZdprUMVA5g'
#find_place()

#geocode()
#places_photo()

def main():
    # csvfile = codecs.open('result.csv', 'r', 'utf_8_sig')
    reader = open('Restaurant.csv',encoding= 'utf-8')
    #csvfile_writer = codecs.open('result_1.csv', 'w+', 'utf_8_sig')
    #writer = csv.writer(csvfile_writer)
    query_fields = "formatted_address"+','+"geometry"+','+"name"+','+"types"+','+"photos"
    i= 0
    output = list()
    for item in reader:

        info = item.split(',')[0]
        input_query = info +' '+'Munich'
        params = {
            'input': input_query,
            'inputtype': 'textquery',
            'fields': query_fields,
            'location_bias' : 'point',
            'key': key
        }
        url = base_url + urlencode(params)
        print(input_query)
        response = urllib.request.urlopen(url)
        jsonRaw = response.read()
        jsonData = json.loads(jsonRaw.decode())
        dict = {
            "type": "Feature",
            "properties": {},
            "geometry": {"type": "Point"}
        }
        if jsonData['status'] == 'OK':

            lat = jsonData['candidates'][0]['geometry']['location']['lat']
            lng = jsonData['candidates'][0]['geometry']['location']['lng']
            coordinate = [lng, lat]
            dict["geometry"]["coordinates"] = coordinate
            dict["properties"]['name'] = jsonData['candidates'][0]['name']
            dict["properties"]['Address'] = jsonData['candidates'][0]['formatted_address']
            dict["properties"]['type'] = "Restaurant"

            #dict["properties"]['photo'] = jsonData['candidates'][0]['photos'][0]['photo_reference']
            output.append(dict)
            i= i+1
            print(i)
            #print (jsonData['candidates'][0]['name'])
    print(i)
    file = open('Restaurant.json', 'w', encoding='utf-8')
    file.write(json.dumps(output, ensure_ascii=False))
    file.close()

main()