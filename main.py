#! /usr/bin/env python
#
# Copyright 2019 Quentin Kniep <hello@quentinkniep.com>
# Distributed under terms of the MIT license.

import os.path
from threading import Thread
import time
import urllib.parse

from bottle import redirect, route, run, view
import ffmpeg_normalize
import googleapiclient.discovery as google
from mpv import MPV
import pafy

import config


player = MPV(ytdl=True, video=False)
youtube = google.build('youtube', 'v3', developerKey=config.YOUTUBE_API_KEY)

queue = [['_KhsQ3nn6Kw', 'Wankelmut & Emma Louise - My Head Is A Jungle (MK Remix)', '', True]]
currentlyPlaying = ['vzYYW8V3Ibc', 'Nothing', 'Nothing', False]
soundEffects = [
        ('iYVO5bUFww0', 'Laughter'),
        ('RktX4lbe_g4', 'Awkward Crickets'),
        ('7ODcC5z6Ca0', 'Sad Violin'),
        ('mVqwnMc1E5M', 'Oooohh'),
        ('6zXDo4dL7SU', 'Ba Dum Tsss'),
        ('n67YJ7ICh_Q', 'Karnevals Tusch'),
        ('5jcOgP-zeTg', 'Gasp'),
        ('y1U6g-kJ5og', 'Booing'),
        ('HnK28w1soPg', 'Kimmunicator'),
        ('cphNpqKpKc4', 'Dun Dun Dunnn'),
        ('Q100Dgdl_rU', 'Sarcastic Laugh'),
        ('Gyu82WG_edM', 'Applause'),
]


def urlEnc(title):
    return urllib.parse.quote(urllib.parse.quote(title, safe=''))


def urlDec(title):
    return urllib.parse.unquote(urllib.parse.unquote(title))


def youtubeSearch(query, maxres, recs=False):
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
            videos.append([search_result['id']['videoId'],
                           search_result['snippet']['title'],
                           urlEnc(search_result['snippet']['title'])])

    return videos


def download(ytid):
    v = pafy.new(ytid)
    s = v.getbest()
    filename = None
    while filename == None:
        try:
            filename = s.download(filepath='downloads/'+ytid)
        except:
            pass
    print('DOWNLOADED ' + ytid + ' into ' + filename)

    if config.ENABLE_VOLUME_NORMALIZATION:
        ffmpnorm = ffmpeg_normalize._ffmpeg_normalize.FFmpegNormalize(
                audio_codec='libmp3lame', output_format='mp3',
                video_disable=True, subtitle_disable=True, target_level=-13)
        ffmpnorm.add_media_file('downloads/'+ytid, 'downloads/'+ytid)
        ffmpnorm.run_normalization()
        print('NORMALIZED ' + ytid)

    return filename


@route('/')
@view('templates/main')
def index():
    return dict(videos=queue, numVids=len(queue), current=currentlyPlaying, volume=int(player.volume))


@route('/search/<keyword>')
@view('templates/results')
def index(keyword):
    keyword = urlDec(keyword)
    vids = youtubeSearch(keyword, 50)
    return dict(videos=vids, header='Search Results', subheader='For: '+keyword)


@route('/rec/<ytid>/<title>')
@view('templates/results')
def index(ytid, title):
    title = urlDec(title)
    vids = youtubeSearch(ytid, 50, recs=True)
    return dict(videos=vids, header='Recommendations', subheader='Based on: '+title)


@route('/add/<ytid>/<title>')
@view('templates/added')
def index(ytid, title):
    title = urlDec(title)
    alreadyDownloaded = False
    if os.path.isfile('downloads/'+ytid):
        alreadyDownloaded = True
    queue.append([ytid, title, urlEnc(title), alreadyDownloaded])
    return dict()


@route('/remove/<ytid>')
def index(ytid):
    global queue
    queue = list(filter(lambda x: x[0] != ytid, queue))
    return redirect('/')


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
    path = 'downloads/' + ytid
    if not os.path.isfile(path):
        download(ytid)
    player.play(path)
    player.wait_for_playback()


def playLoop():
    global currentlyPlaying
    while True:
        if not queue:
            currentlyPlaying = youtubeSearch(currentlyPlaying[0], 10, recs=True)[0]
            play(currentlyPlaying[0])
        else:
            if not queue[0][3]:  # wait for download to finish
                time.sleep(1)
                continue
            currentlyPlaying = queue[0]
            del queue[0]
            play(currentlyPlaying[0])


def downloadLoop():
    while True:
        for i in range(len(queue)):
            if not queue[i][3]:
                download(queue[i][0])
                queue[i][3] = True
        time.sleep(1)


if __name__ == '__main__':
    playThread = Thread(target=playLoop)
    playThread.start()

    downloadThread = Thread(target=downloadLoop)
    downloadThread.start()

    pafy.set_api_key(config.YOUTUBE_API_KEY)
    run(host=config.HOST_NAME, port=config.PORT_NUMBER, server=config.SERVER_TYPE)
