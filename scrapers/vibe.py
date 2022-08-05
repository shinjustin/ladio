import json
import requests
from pprint import pprint

url = 'https://apis.naver.com/vibeWeb/musicapiweb/vibe/v1/chart/track/total?display=100'
headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
        'accept': 'application/json',
        }
r = requests.get(url, headers=headers).json()
chart = r['response']['result']['chart']['items']['tracks']
songs = list()
for song in chart:
    rank = song['rank']['currentRank']
    title = song['trackTitle']
    artists = song['artists']
    if len(artists) > 1:
        artists = [artist['artistName'] for artist in artists]
    else:
        artists = [artists[0]['artistName']]
    album = song['album']['albumTitle']
    likes = song['likeCount']
    image = song['album']['imageUrl']

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
with open('vibe.json', 'w') as f:
    json.dump(songs, f)
