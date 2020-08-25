# -*- coding: utf-8 -*-
#
# Copyright 2020 Quentin Kniep <hello@quentinkniep.com>
# Distributed under terms of the MIT license.

import urllib.parse

import googleapiclient.discovery as google

import config


def url_enc(title):
    return urllib.parse.quote(urllib.parse.quote(title, safe=''))


def url_dec(title):
    return urllib.parse.unquote(urllib.parse.unquote(title))


class YoutubeWrapper:
    def __init__(self):
        self.api = google.build('youtube', 'v3', developerKey=config.YOUTUBE_API_KEY)

    def search(self, query, maxres, recs=False):
        if recs:
            search_response = self.api.search().list(
                relatedToVideoId=query,
                part='id,snippet',
                maxResults=maxres,
                type='video',
                topicId='/m/04rlf',
            ).execute()
        else:
            search_response = self.api.search().list(
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
