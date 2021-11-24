
# %%
import requests
url = 'https://static.wikia.nocookie.net/onepiece/images/a/ad/Chapter_156.png/revision/latest?cb = 20130121043120'
r = requests.head(url)

print(r.headers)



# %%
