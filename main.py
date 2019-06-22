#! /usr/bin/env python
#
# Copyright 2019 Quentin Kniep <hello@quentinkniep.com>
# Distributed under terms of the MIT license.

from bottle import redirect, route, run, template, view
from googleapiclient.discovery import build
from threading import Thread
import urllib.parse
import mpv
import pafy
import random
import time

import cfg


YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

player = mpv.MPV(ytdl=True, video=False)

queue = []
currentlyPlaying = ['vzYYW8V3Ibc', 'Nothing', 'Nothing']
sitcomEffects = [
        'iYVO5bUFww0',  # laughter
        'RktX4lbe_g4',  # awkward crickets
        '7ODcC5z6Ca0',  # sad violin
        'mVqwnMc1E5M',  # ooooh
        '6zXDo4dL7SU',  # ba dum tsss
        'n67YJ7ICh_Q',  # karnevals tusch
        '5jcOgP-zeTg',  # gasp
        'y1U6g-kJ5og',  # booing
        'HnK28w1soPg',  # Kim Possible
        'cphNpqKpKc4',  # dun dun dunnn
        'Q100Dgdl_rU',  # sarcastic laugh
        'Gyu82WG_edM'   # clapping
]


def urlEnc(title):
    return urllib.parse.quote(urllib.parse.quote(title, safe=''))


def urlDec(title):
    return urllib.parse.unquote(urllib.parse.unquote(title))


def youtube_search(query, maxres, recs=False):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=cfg.YOUTUBE_API_KEY)

    if recs:
        search_response = youtube.search().list(
            relatedToVideoId=query,
            part='id,snippet',
            maxResults=maxres,
            type='video',
            topicId='/m/04rlf',
        ).execute()
    else:
        search_response = youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=maxres,
            type='video',
            topicId='/m/04rlf',
        ).execute()

    videos = []

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append((search_result['id']['videoId'],
                           search_result['snippet']['title'],
                           urlEnc(search_result['snippet']['title'])))

    return videos


def download(ytid):
    v = pafy.new(ytid)
    s = v.getbest()
    filename = s.download()
    return filename


@route('/search/<keyword>')
@view('templates/results')
def index(keyword):
    vids = youtube_search(keyword, 50)
    return dict(videos=vids, header='Search Results', subheader='For: '+keyword)


@route('/rec/<ytid>/<title>')
@view('templates/results')
def index(ytid, title):
    vids = youtube_search(ytid, 50, True)
    return dict(videos=vids, header='Recommendations', subheader='Based on: '+urlDec(title))


@route('/add/<ytid>/<title>')
@view('templates/added')
def index(ytid, title):
    queue.append((ytid, urlDec(title), title))
    return dict()


@route('/remove/<ytid>')
def index(ytid):
    global queue
    queue = list(filter(lambda x: x[0] != ytid, queue))
    return redirect('/')


@route('/')
@view('templates/main')
def index():
    return dict(videos=queue, numVids=len(queue), current=currentlyPlaying, volume=int(player.volume))


@route('/skip')
def index():
    player.seek(100, 'absolute-percent')
    return redirect('/')


@route('/volume/<vol>')
def index(vol):
    if int(vol) > player.volume_max:
        player.volume = player.volume_max
    else:
        player.volume = vol
    return redirect('/')


def play(ytid):
    player.play('https://youtu.be/' + ytid)
    player.wait_for_playback()


def playLoop():
    global currentlyPlaying
    while True:
        if not queue:
            effect = random.choice(sitcomEffects)
            play(effect)
        else:
            currentlyPlaying = queue[0]
            del queue[0]
            play(currentlyPlaying[0])


if __name__ == '__main__':
    t = Thread(target=playLoop)
    t.start()
    #pafy.set_api_key(cfg.YOUTUBE_API_KEY)
    run(host=cfg.HOST_NAME, port=cfg.PORT_NUMBER)
