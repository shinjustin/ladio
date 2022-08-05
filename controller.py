import json
from fuzzywuzzy import fuzz, process
from pprint import pprint

#url = 'https://m.bugs.co.kr/search/track?q='

chart = list()

def find_song_index(title, artists):
    for song in chart:
        if song['title'] == title and song['artists'] == artists:
            index = chart.index(song)
            return index

def extractOne(string, candidate_list):
    best = ('', 0)
    for song in chart:
        db_string = song.get('db_string')
        ratio = fuzz.ratio(string, db_string)
        if ratio > best[1]:
            best = (db_string, ratio)
    return best



def aggregate(songs):
    for song in songs:
        title = song['title']
        artists = song['artists']
        score = ((len(songs) + 1 - int(song['rank'])))
        # special string to plug into temporary database
        db_string = f'{", ".join(artists)} - {title}'

        # find if it exists in db
        candidate_list = [f'{", ".join(song["artists"])} - {song["title"]}' for song in chart]
        candidate = extractOne(db_string, candidate_list)
        if candidate:
            if candidate[1] == 100:
                index = find_song_index(title, artists)
                chart[index]['score'] += score
            elif candidate[1] >= 90:
                # find song in chart
                song = [song for song in chart if song['db_string'] == candidate[0]][0]
                index = chart.index(song)
                #index = find_song_index(new_title[0], artists)
                chart[index]['score'] += score
            else:
                # append new chart song
                song = {
                        'title': title,
                        'artists': artists,
                        'score': score,
                        'db_string': db_string,
                        }
                chart.append(song)
        else:
            # append new chart song
            song = {
                    'title': title,
                    'artists': artists,
                    'score': score,
                    'db_string': db_string,
                    }
            chart.append(song)


def main():
    sources = [
            'bugs',
            'genie',
            'melon',
            'vibe',
            ]
    for source in sources:
        with open(f'scrapers/{source}.json', 'r') as f:
            songs = json.load(f)
        aggregate(songs)

    new_list = sorted(chart, key=lambda d: d['score'], reverse=True)
    for song in new_list:
        song['score'] /= len(sources)
    pprint(new_list[0:25])
    return chart

if __name__ == '__main__':
    main()
