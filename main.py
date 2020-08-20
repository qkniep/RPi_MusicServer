# -*- coding: utf-8 -*-
#
# Copyright 2020 Quentin Kniep <hello@quentinkniep.com>
# Distributed under terms of the MIT license.

import os.path
from threading import Thread
import urllib.parse

from flask import Flask, redirect, render_template, url_for
import googleapiclient.discovery as google

import config


app = Flask(__name__)
youtube = google.build('youtube', 'v3', developerKey=config.YOUTUBE_API_KEY)


def url_enc(title):
    return urllib.parse.quote(urllib.parse.quote(title, safe=''))


def url_dec(title):
    return urllib.parse.unquote(urllib.parse.unquote(title))


def youtube_search(query, maxres, recs=False):
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
                           url_enc(search_result['snippet']['title'])])
    return videos


@app.route('/')
def index():
    return render_template('main.html', videos=queue,
                           numVids=len(queue), current=currentlyPlaying,
                           # volume=int(player.volume))
                           volume=100)


@app.route('/search/<keyword>')
def search_results(keyword):
    keyword = url_dec(keyword)
    vids = youtube_search(keyword, 50)
    return render_template('results.html', videos=vids,
                           header='Search Results', subheader='For: '+keyword)


@app.route('/rec/<ytid>/<title>')
def yt_recommendations(ytid, title):
    title = url_dec(title)
    vids = youtube_search(ytid, 50, recs=True)
    return render_template('results.html', videos=vids,
                           header='Recommendations',
                           subheader='Based on: '+title)


@app.route('/add/<ytid>/<title>')
def add_song(ytid, title):
    title = url_dec(title)
    already_downloaded = False
    if os.path.isfile('downloads/'+ytid):
        already_downloaded = True
    queue.append([ytid, title, url_enc(title), already_downloaded])
    return render_template('added')


@app.route('/remove/<ytid>')
def remove_song(ytid):
    global queue
    queue = list(filter(lambda x: x[0] != ytid, queue))
    return redirect(url_for('/'))


# @app.route('/skip')
# def skip_song():
#     player.seek(100, 'absolute-percent')
#     return redirect(url_for('/'))


# @app.route('/volume/<vol>')
# def change_volume(vol):
#     if int(vol) > player.volume_max:
#         player.volume = player.volume_max
#     else:
#         player.volume = vol
#     return redirect(url_for('/'))
