# Music Server for Raspberry Pi

Works with YouTube and Spotify.

[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/quality/g/qkniep/RPi_MusicServer)](https://scrutinizer-ci.com/g/qkniep/RPi_MusicServer)
[![Maintainability](https://api.codeclimate.com/v1/badges/3acb1089cfdb0a59eb34/maintainability)](https://codeclimate.com/github/qkniep/RPi_MusicServer/maintainability)
[![CodeFactor](https://www.codefactor.io/repository/github/qkniep/rpi_musicserver/badge)](https://www.codefactor.io/repository/github/qkniep/rpi_musicserver)

With this project I aim to provide a software which can be hosted on a Raspberry Pi and operates as a collaborative music server.
The server can be accessed via a web browser from any device which can communicate with the RPi over the internet.
I am also working on advanced features to provide a better collaborative experience.

## Features / Roadmap
* [x] YouTube Search
* [x] Auto-Play Recommendations
* [x] Collaborative Queue
* [ ] Spotify Search
* [ ] Default Config
* [ ] Config in YAML, TOML, JSON, or something
* [ ] Playlists
* [ ] Security Measures (Authentication)
* [ ] Song Voting
* [ ] Automatic Volume Adjustment (YT)
* [ ] Mix Playlists

## Dependencies
This software requires Python 3 and the following Python libraries:
* [Bottle](https://bottlepy.org/docs/stable) 0.12.18
* [Google API Client](https://googleapis.github.io/google-api-python-client) 1.10.0
* [Pafy](https://pypi.org/project/pafy)
* [python-mpv](https://github.com/jaseg/python-mpv) 0.5.2
* [spotipy](https://github.com/plamere/spotipy) 2.13.0

Highly recommended, but not stricly necessary is:
* [Paste](https://pypi.org/project/Paste) 3.4.3

**All Depencies can be installed through pipenv.**

## Setup
You need to write a `config.py` file like the following:
```python
HOST_NAME = 'XXX.XXX.XXX.XXX'
PORT_NUMBER = 7000
SERVER_TYPE = 'paste'

ENABLE_VOLUME_NORMALIZATION = False

YOUTUBE_API_KEY = 'AIza...'
```
Put this file in the root directory of the music server.
You'll need to replace the `HOST_NAME` variable with your servers IP address,
and set the `YOUTUBE_API_KEY` variable to a valid key for the [YouTube Data API](https://developers.google.com/youtube/v3).
If you did not download the recommended server software *'Paste'*,
you have to change the `SERVER_TYPE` to the server you want to use instead,
a list of possibilities can be found in the [Bottle Documentation](https://bottlepy.org/docs/stable/deployment.html#switching-the-server-backend).

Then, assuming that the music server is located in a directory called *'musicServer'*,
you can run it using the `supervise` command from the parent directory:
```bash
$ nohup supervise musicServer &
```
The `nohup` command prevents the server from shutting down when you log out of the shell that launched it.
Whereas the `supervise` command will automatically relaunch the server if/when it crashes.
Therefore the command above should lead to the server being up until you explicitly decide to kill the program.

## License
This project is licensed under the [MIT License](LICENSE).
