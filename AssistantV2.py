import threading
import numpy as np


class Assistant(threading.Thread):
    def __init__(self):
        self.running = True
        self.dirs = read_dirs()
        self.notes = read_notes()
        self.functions = {
            'sc': self.create_sc
        }

    def run(self):
        while self.running is True:
            input_cmd = input('>> ')
            self.handle_input(input())

    def create_sc(self):
        print('dasdsad')

    def handle_input(self, cmd):
        if self.valid_command(cmd) is True:
            self.functions[cmd]()

    def valid_command(self, cmd) -> bool:
        for f in self.functions:
            if cmd == f:
                return True
        return False


def read_notes() -> dict:
    return np.load(r'\data\notes.npy', allow_pickle=True).item()


def read_dirs() -> dict:
    return np.load(r'\data\dirs.npy', allow_pickle=True).item()


a = Assistant()
a.start()
