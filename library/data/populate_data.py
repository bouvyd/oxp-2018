from googleapiclient.discovery import build
import os
from pprint import pprint
import requests
import xml.etree.cElementTree as ET


API_KEY = "AIzaSyBAX4ZnZLHgKL9XdjLdJ3N0B4P3l6WhUjQ"
IMG_PATH = '../static/img/'


isbn_list = ["9780765388971", "9780553803723", "9780553803730", "9782266079990", "9780345453747",
             "9780553803716", "9780345418975", "9780804139021", "9781500453305", "9780765316974",
             "9780765354068", "9780765316981", "9780765333513", "9780765376077", "9780752224411",
             "9780765316998", "9781596061033", "9781444727333", "9780765382153", "9780356502427",
             "9780316246651", "9780316246620", ]

service = build('books', 'v1', developerKey=API_KEY)
book_data = dict.fromkeys(isbn_list)
root = ET.Element("odoo")

for isbn in isbn_list:
    pprint('fetching %s' % isbn)
    r = service.volumes().list(q='isbn:{0}'.format(isbn)).execute()
    if r.get('totalItems', 0) > 0:
        r = r['items'][0]['volumeInfo']
        volume_id = r['canonicalVolumeLink'].split('=')[-1]
        r = service.volumes().get(volumeId=volume_id).execute()['volumeInfo']
        if r.get('imageLinks'):
            response = requests.get(r['imageLinks']['thumbnail'])
            if response.ok:
                img_path = os.path.join(IMG_PATH,'%s.jpg' % isbn)
                with open(img_path, "wb") as img_file:
                    img_file.write(response.content)
        else:
            continue
        data = {
            'title': r['title'],
            'author': ','.join(r['authors']),
            'summary': r['description'],
            'isbn': isbn,
            'image': 'library/static/img/%s.jpg' % isbn,
        }
        record = ET.SubElement(root, "record", attrib={'model': 'library.book', 'id': isbn})
        for field,value in data.items():
            f = ET.SubElement(record, "field", attrib={'name': field})
            if field == 'image':
                f.set('type', 'base64')
                f.set('file', value)
            else:
                f.text = value

xmldata = ET.tostring(root)  
with open("demo.xml", "wb") as demo_file:
    demo_file.write(xmldata)  