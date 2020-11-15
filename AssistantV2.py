import re
import threading
import urllib
import vlc
import numpy as np
import webbrowser

import pafy
import requests


class Assistant(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.dirs = read_dirs()
        self.notes = read_notes()
        self.current_site = ''
        self.current_song = ''
        self.video = None
        self.best = None
        self.media = None
        self.functions = {
            'sc': self.create_shortcut,
            'w': self.open_web,
            'p': self.play_song,
            'v': self.control_volume,
            'n': self.handle_n
        }

    def run(self):
        while self.running is True:
            input_cmd = input('>> ')
            self.handle_input(input_cmd)

    def control_volume(self):
        input_cmd = input('mute/play/#: ')
        if input_cmd == 'mute':
            vlc.MediaPlayer.audio_set_mute(self.media, True)  # Mute
        elif input_cmd == 'play':
            vlc.MediaPlayer.audio_set_mute(self.media, False)  # Resume
        else:
            volume = int(input_cmd)
            vlc.MediaPlayer.audio_set_volume(self.media, volume)  # set volume to int value

    def play_song(self) -> vlc.MediaPlayer:  # returns instance of MediaPlayer
        song_name = input('Enter Song Name: ')
        self.video = pafy.new(find_song_url(song_name))
        self.best = self.video.getbestaudio()
        if self.media is not None:
            vlc.MediaPlayer.release(self.media)
        self.media = vlc.MediaPlayer(self.best.url)
        vlc.MediaPlayer.audio_set_volume(self.media, 50)
        self.media.play()  # play YouTube audio
        return self.media

    def handle_n(self):
        n = input("Enter Note: ")
        title = input("Enter Title: ")
        self.note[title] = n
        self.save()
        print("Saved Note: ", {title})

    def open_web(self):
        self.current_site = input("Enter Site URL: ")
        webbrowser.open(self.current_site)
        print("Starting Browser: ", {self.current_site})

    def create_shortcut(self):
        path = input("Enter Dir. Path: ")
        alias = input("Enter Dir. Alias: ")
        self.dirs[alias] = path
        self.save()
        print("Saved ShortCut: ", {alias}, " ~ ", {path})

    def handle_input(self, cmd):
        if self.valid_command(cmd) is True:
            self.functions[cmd]()

    def valid_command(self, cmd) -> bool:
        for f in self.functions:
            if cmd == f:
                return True
        return False

    def save(self):
        np.save('dirs.npy', self.dirs)
        np.save('notes.npy', self.notes)
        print("Force Save ALL!")


def find_song_url(song_name) -> str:
    query_string = urllib.parse.urlencode({"search_query": song_name})
    format_url = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
    search_results = re.findall(r"watch\?v=(\S{11})", format_url.read().decode())
    clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(search_results[0]))
    format_clip = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])  # refined YouTube video URL
    return format_clip


def read_notes() -> dict:
    return np.load('notes.npy', allow_pickle=True).item()


def read_dirs() -> dict:
    return np.load('dirs.npy', allow_pickle=True).item()


a = Assistant()
a.start()
