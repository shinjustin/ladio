import urllib
import json
import requests
import urllib
from bs4 import BeautifulSoup
from pprint import pprint

def extract(date=None):
    url = 'https://www.genie.co.kr/chart/top200?ditc=D&rtm=N'
    headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0'
            }
    if date:
        # date format: YYYMMDD (e.g. 20220802)
        url += f'&ymd={date}'
    print(url)
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    song_ids = soup.find('input', id='sAllSongID')['value']
    # returns 201 items; last one is blank
    song_ids = song_ids.split(';')
    songs = list()
    for i in range(100):
        song_id = song_ids[i]
        params = {
            "sq": "1",
            "xgnm": song_id,
            "bit": "192",
            "uxnm": "",
            "uxtk": "",
            "ualt": "",
            "cdm": "hls",
            "previewYn": "Y"
        }

        song_url = 'https://www.genie.co.kr/player/playStmInfo.json'
        r = requests.post(song_url, headers=headers, data=params).json()
        data = r['DATA0']
        # convert html entities to string
        rank = i+1
        title = data['SONG_NAME']
        title = urllib.parse.unquote(title)
        artists = data['ARTIST_NAME']
        artists = urllib.parse.unquote(artists)
        if '&' in artists:
            artists = artists.split(' & ')
        else:
            artists = [artists]
        album = data['ALBUM_NAME']
        album = urllib.parse.unquote(album)
        likes = data['SONG_LIKE_CNT']
        image = data['ABM_IMG_PATH']
        image = urllib.parse.unquote(image)
        image = 'https:' + image
        song = {
                'rank': rank,
                'title': title,
                'artists': artists,
                'album': album,
                'likes': likes,
                'image': image,
                }
        songs.append(song)
        pprint(song)
    with open('genie.json', 'w') as f:
        json.dump(songs, f)

if __name__ == '__main__':
    import sys
    date = None
    if len(sys.argv) > 1:
        date = sys.argv[1]
    extract(date)
