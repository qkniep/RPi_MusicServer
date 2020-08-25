# -*- coding: utf-8 -*-
#
# Copyright © 2020 Quentin Kniep <hello@quentinkniep.com>
# Distributed under terms of the MIT license.
"""Manages playback through multiple audio players.
Currently supports: Spotify, MPV (for YouTube).
"""

import json
import os.path
import time
from threading import Thread

import ffmpeg_normalize
from mpv import MPV
import pafy
import spotipy

import config
from util import YoutubeWrapper


class Player:
    def __init__(self):
        self.queue = [['_KhsQ3nn6Kw', 'Wankelmut & Emma Louise - My Head Is A Jungle (MK Remix)', '', True]]
        self.current_track = ['vzYYW8V3Ibc', 'Nothing', 'Nothing', False]

        self.player = MPV(ytdl=True, video=False)
        self.youtube = YoutubeWrapper()

        sp_oauth = spotipy.oauth2.SpotifyOAuth(scope=config.SPOTIPY_SCOPE,
                                               cache_path=config.SPOTIPY_CACHE)

        self.spotify = spotipy.Spotify(auth_manager=sp_oauth)

        devices = self.spotify.devices()
        print(json.dumps(devices, sort_keys=True, indent=4))
        device_id = devices['devices'][0]['id']

        results = self.spotify.search(q='Airwaves', type='track')
        print(json.dumps(results['tracks']['items'][0], sort_keys=True, indent=4))
        self.spotify.start_playback(device_id, uris=[results['tracks']['items'][0]['uri']])

    def play_loop(self):
        while True:
            if not self.queue:
                next_track = self.youtube.search(self.current_track[0], 1, recs=True)[0]
                self.current_track = next_track
                self.play(next_track[0])
            else:
                if not self.queue[0][3]:  # wait for download to finish
                    time.sleep(1)
                    continue
                self.current_track = self.queue[0]
                del self.queue[0]
                self.play(self.current_track[0])

    def download_loop(self):
        while True:
            for entry in self.queue:
                if not entry[3]:
                    self.download(entry[0])
                    entry[3] = True
            time.sleep(1)

    def download(self, ytid):
        video = pafy.new(ytid)
        stream = video.getbestaudio()
        filename = None
        while filename is None:
            try:
                filename = stream.download(filepath='downloads/'+ytid,
                                           quiet=True)
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

    def play(self, ytid):
        path = 'downloads/' + ytid
        if not os.path.isfile(path):
            self.download(ytid)
        self.player.play(path)
        self.player.wait_for_playback()

    def run(self):
        play_thread = Thread(target=self.play_loop)
        play_thread.start()

        download_thread = Thread(target=self.download_loop)
        download_thread.start()

        pafy.set_api_key(config.YOUTUBE_API_KEY)
