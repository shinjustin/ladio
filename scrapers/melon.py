import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint

url = 'https://www.melon.com/chart/day/index.htm'
likes_url = 'https://www.melon.com/commonlike/getSongLike.json?contsIds='
# requires user agent to load page
headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0'
        }
html = requests.get(url, headers=headers).text
soup = BeautifulSoup(html, 'lxml')
rows = soup.find('tbody').find_all('tr')
songs = list()
song_ids = list()
for row in rows:
    song_id = row['data-song-no']
    song_ids.append(song_id)
    cols = row.find_all('td')

    rank = cols[1].find('span', class_='rank').string
    image = cols[3].find('img')['src']
    title = cols[5].find('div', class_='wrap_song_info').find('div', class_='ellipsis rank01').find('a').string
    artists = cols[5].find('div', class_='wrap_song_info').find('div', class_='ellipsis rank02')
    artists.find('span', class_='checkEllipsis').decompose()
    artists = artists.find_all('a')
    artists = [artist.string for artist in artists]
    album = cols[6].find('div', class_='ellipsis rank03').find('a').string
    likes = cols[7].find('span', class_='cnt').string
    song = {
            'rank': rank,
            'title': title,
            'artists': artists,
            'album': album,
            'image': image,
            }
    songs.append(song)

count = 0
for song_id in song_ids:
    likes_url += song_id
    if count < 99:
        likes_url += '%2C'

    count += 1

count = 0
r = requests.get(likes_url, headers=headers).json()
for song in r['contsLike']:
    likes = song['SUMMCNT']
    songs[count]['likes'] = likes
    count += 1

pprint(songs)
with open('melon.json', 'w') as f:
    json.dump(songs, f)
