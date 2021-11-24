"""
Downloads One Piece color spreads and covers from One Piece Wiki in fandom.com
"""


import itertools
import json
import requests
import urllib.request
from bs4 import BeautifulSoup
import signal
import sys


URLS = ['https://onepiece.fandom.com/wiki/Category:Color_Spreads',
        'https://onepiece.fandom.com/wiki/Category:Color_Covers']
IMG_CLASS = 'category-page__member-thumbnail'


def load_db():
    """
    Load images.json where we store already downloaded images.
    """
    print('reading json')
    try:
        with open("images.json", "rb") as json_file:
            data_imgs = json.load(json_file)
            print(f'{len(data_imgs)} images in db')
            return data_imgs
    except IOError:
        print('Nothing in db')
        return []


def save_db(image_list):
    """
    Saves downloaded images to images.json
    """
    print('saving json')
    with open('images.json', 'w') as j:
        json.dump(image_list, j, indent=4, sort_keys=True)


def list_images(url):
    print('listing imgs')
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.find_all(class_=IMG_CLASS)

    imgs = []
    for link in links:
        if 'data:image' not in link['src']:
            imgs.append({
                'src': link['src'],
                'title': link['alt'],
                'url': url
            })
    return imgs


def download_img(entry):
    download_link = entry['src'][0:entry['src'].find('latest')+7]
    title = entry['src'][entry['src'].find(
        '/Chapter'):entry['src'].find('/revision')]
    urllib.request.urlretrieve(download_link, f'imgs//{title}')
    # return title

# def upload_imgur(file):
#     download_link = entry['src'][0:entry['src'].find('latest')+7]
#     title = entry['src'][entry['src'].find(
#         '/Chapter'):entry['src'].find('/revision')]
#     urllib.request.urlretrieve(download_link, f'imgs//{title}')

#     return title

def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, original_sigint)

    print("Ok ok, quitting")
    save_db(ALREADY_saved)
    sys.exit(1)

    # restore the exit gracefully handler here    
    signal.signal(signal.SIGINT, exit_gracefully)

# %%
if __name__ == '__main__':
    # original_sigint = signal.getsignal(signal.SIGINT)
    # signal.signal(signal.SIGINT, exit_gracefully)
    ALREADY_saved = load_db()
    for URL in URLS:
        images = list_images(URL)
        new_images = list(itertools.filterfalse(lambda x: x in images, ALREADY_saved)) + \
            list(itertools.filterfalse(lambda x: x in ALREADY_saved, images))
        if len(new_images)>0:
            print(f'downloading {len(new_images)} files')
            ALREADY_saved += new_images
            for img in new_images:
                try:
                    download_img(img)
                except:
                    print('error')
                    print(img)
                    pass
        
        # upload_imgur(file)

    save_db(ALREADY_saved)
    print('finished')

# %%
