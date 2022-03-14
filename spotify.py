import os
from pprint import pp, pprint
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import _thread as thread

load_dotenv()
app_id = os.getenv("SPOTIFY_APP_ID")
secret = os.getenv("SPOTIFY_SECRET")
uri = os.getenv("SPOTIFY_URI")
scope = "user-read-private user-read-playback-state user-modify-playback-state user-library-read "


class Player:
    def __init__(self, spotify):
        self.sp = spotify

    def getTrack(self):
        return Track(self.sp.current_user_playing_track())

    def isPlaying(self):
        return self.sp.currently_playing()["is_playing"]

    def play(self):
        self.sp.start_playback()

    def songChange(self, callback):
        track = self.getTrack()
        lastTrack = None
        while self.isPlaying():
            if track.name != lastTrack:
                print(track)
                lastTrack = track.name
                callback(track.lcd())
            track = self.getTrack()

    def playing(self, callback):
        if self.isPlaying():
            print("Playing")
            thread.start_new_thread(self.songChange, callback)


class Track:
    def __init__(self, song_data):
        self.song_data = song_data
        item = song_data["item"]
        self.name = item["name"]
        self.artist = item["artists"][0]["name"]
        self.album = item["album"]["name"]
        self.duration = item["duration_ms"]
        self.uri = item["href"]

    def getProgress(self):
        return self.song_data["progress_ms"]

    def lcd(self):
        return f"{self.name}-{self.artist}\n{self.album}"

    def __getMinutes(self):
        time = self.duration / 60000
        seconds = (time - int(time)) * 60
        return f"{int(time)}:{int(seconds)}"

    def __str__(self):
        return f"{self.name} by {self.artist} from {self.album} - {self.__getMinutes()}"


def initialize():
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=app_id,
            client_secret=secret,
            redirect_uri=uri,
            scope=scope,
        )
    )
    return Player(sp)


def run(player, callback):
    player.playing(callback)
    while True:
        pass


if __name__ == "__main__":
    player = initialize()
    print("Starting")
    player.playing()
    while True:
        pass
# save song in json file for later use
# with open("current_track.json", "w") as f:
# f.write(json.dumps(current_track))
