#%%
"""
Downloads One Piece color spreads and covers from One Piece Wiki at fandom.com
"""
import requests
from bs4 import BeautifulSoup
from pysondb import db
from one_piece_color.gphotos import upload_photos, auth
from one_piece_color.download import download_file

ALBUM_ID = 'AMQn-3ZPXaYZq6laEwY7KfBpCV9BzEVr7cVEm0lammX_i5cZucjZVsTgbuPWm9CIHgjQOT3aQP3O'
DB_FILE = 'images.json'

URLS = [
    [ 'https://onepiece.fandom.com/wiki/Category:Color_Spreads', 'Color Spreads' ],
    [ 'https://onepiece.fandom.com/wiki/Category:Color_Covers', 'Color Covers' ]
]

CLASS_NAME = 'category-page__member-thumbnail'

def main(url, color_type, img_db, service):
    webpage = requests.get(url).text

    soup = BeautifulSoup(webpage, 'html.parser')

    img_list = soup.findAll('img', {'class': CLASS_NAME})

    for img in img_list:
        print(img['alt'])
        data = {
            'src': img['src'][0:img['src'].find('latest')+6],
            'chapter': img['alt'].replace('.png', ''),
            'filename': img['alt'],
            'type': color_type
        }
        if not img_db.getByQuery({'filename': data['filename']}):
            print('uploading')
            download_file(data['src'], data['filename'])
            upload_photos(service, f"images/{data['filename']}", ALBUM_ID)
            img_db.add(data)


if __name__ == '__main__':
    img_db = db.getDb(DB_FILE)
    service, creds = auth()

    for url in URLS:
        main(url[0], url[1], img_db, service)

# %%
