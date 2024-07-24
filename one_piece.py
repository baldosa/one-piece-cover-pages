# %%
"""
Downloads One Piece color spreads and covers from One Piece Wiki at fandom.com
"""
import requests
import json
from bs4 import BeautifulSoup
from download import download

ALBUM_ID = (
    "AMQn-3ZPXaYZq6laEwY7KfBpCV9BzEVr7cVEm0lammX_i5cZucjZVsTgbuPWm9CIHgjQOT3aQP3O"
)
DB_FILE = "images.json"

URLS = [
    ["https://onepiece.fandom.com/wiki/Category:Color_Spreads", "Color Spreads"],
    ["https://onepiece.fandom.com/wiki/Category:Color_Covers", "Color Covers"],
]

CLASS_NAME = "category-page__member-thumbnail"


def gen_img_dict(url, color_type):
    webpage = requests.get(url).text

    soup = BeautifulSoup(webpage, "html.parser")

    img_list = soup.findAll("img", {"class": CLASS_NAME})
    img_dicts = []

    for img in img_list:
        data = {
            "src": img["src"][0 : img["src"].find("latest") + 6],
            "chapter": img["alt"].replace(".png", ""),
            "filename": img["alt"],
            "type": color_type,
        }
        img_dicts.append(data)
    return [i for n, i in enumerate(img_dicts) if i not in img_dicts[:n]]


# %%
if __name__ == "__main__":
    # list all images on URLS
    img_dicts = []
    for url in URLS:
        img_dicts = img_dicts + (gen_img_dict(url[0], url[1]))

    # check if images was already downloaded
    parsed_file = json.load(open(DB_FILE))

    to_download = [x for x in img_dicts if x not in parsed_file]

    # download new images
    downloaded = []
    for d in to_download:
        try:
            download(d["src"], "images/", d["filename"])
            downloaded.append(d)

        except Exception as e:
            print(e)
            pass

    with open(DB_FILE, "w") as f:
        json.dump(parsed_file + downloaded, f)


# print(img_dicts)
