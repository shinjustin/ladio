import json
import re
import requests
from bs4 import BeautifulSoup
from pprint import pprint

url = 'https://m.bugs.co.kr/chart/track/day/all'
html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')
songs = list()

regex = 'window\.__INITIAL_STATE__\=(.*)'
scripts = soup.find_all('script')
script = scripts[5].string
script = re.search(regex, script)[1]
script = script.replace(';', '')
script = json.loads(script)
chart_list = script['1']['data']['chartList']
for song in chart_list:
    rank = song['list_attr']['rank']
    artists = list()
    for attr in song['artists']:
        artist = attr['artist_nm']
        artists.append(artist)
    title = song['track_title']
    album = song['album']['title']
    likes = song['adhoc_attr']['likes_count']
    image_size = 200
    image_url = f'https://image.bugsm.co.kr/album/images/{image_size}'
    image = song['album']['image']['path']
    image = image.replace('\\u002F', '/')
    image = image_url + image
    song = {
            'rank': rank,
            'title': title,
            'artists': artists,
            'album': album,
            'likes': likes,
            'image': image,
            }
    songs.append(song)
    pprint(songs)
with open('bugs.json', 'w') as f:
    json.dump(songs, f)
