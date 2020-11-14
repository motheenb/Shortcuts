import webbrowser
import webbrowser
import numpy as np
import re, requests, subprocess, urllib.parse, urllib.request
from bs4 import BeautifulSoup

# @Author (Motheen Baig)
# GitHub (https://github.com/motheenb/Shortcuts)


def main():
    load_operations()
    listen(True)


def listen(running):  # listens for user input
    while running:
        user_input = input(">> ")
        handle_input(user_input)


def load_operations():
    ops.append("sc")  # create short-cut.
    ops.append("p")  # play youtube song
    ops.append("o")  # open alias dir.
    ops.append("w")  # open web URL
    ops.append("n")  # make sticky notes
    ops.append("s")  # save ALL


def valid_command(op) -> bool:
    if op in ops:
        return True
    else:
        print("Invalid operation!!")
        return False


def handle_input(operation) -> bool:
    if valid_command(operation):
        funcs[operation]()
        return True
    return False


def note_exists(n) -> bool:
    if n in note:
        return True
    else:
        print("Note not found!")
        return False


def alias_exists(alias) -> bool:
    if alias in dirs:
        return True
    else:
        print("Alias not found!")
        return False


def handle_lol():
    site = input("'o' for op.gg, 'p' for professor.gg: ")
    lol_name = input("Enter Player/Champ. name: ")
    url = ""
    if site == 'p':
        url = "https://porofessor.gg/live/na/" + lol_name
    elif site == 'o':
        url = "https://na.op.gg/champion/" + lol_name + "/statistics/jungle"
    print("Opening: {" + url + "}")
    webbrowser.open(url)


def handle_n():
    n = input("Enter Note: ")
    title = input("Enter Title: ")
    note[title] = n
    save()
    print("Saved Note: ", {title})


def handle_o():
    alias = input("Enter Alias/Title: ")
    if alias_exists(alias):
        subprocess.Popen([dirs[alias]])
        print("Opening: ", {dirs[alias]})
    elif note_exists(alias):
        print("Opening Note: ", {alias})
        print(note[alias])


def handle_p():
    song_name = input("Enter Song Name: ")
    query_string = urllib.parse.urlencode({"search_query": song_name})
    format_url = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
    search_results = re.findall(r"watch\?v=(\S{11})", format_url.read().decode())
    clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(search_results[0]))
    format_clip = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
    inspect = BeautifulSoup(clip.content, "html.parser")
    title = inspect.find_all("meta", property="og:title")
    for concatMusic1 in title:
        pass
    print("Playing: ", {concatMusic1['content']})
    webbrowser.open(format_clip)


def handle_sc():
    path = input("Enter Dir. Path: ")
    alias = input("Enter Dir. Alias: ")
    dirs[alias] = path
    save()
    print("Saved ShortCut: ", {alias}, " ~ ", {path})


def open_web():
    url = input("Enter Site URL: ")
    webbrowser.open(url)
    print("Starting Browser: ", {url})


def save():
    np.save('C:/py/dirs.npy', dirs)
    np.save('C:/py/notes.npy', note)
    print("Force Save ALL!")


def read_notes() -> dict:
    return np.load('C:/py/notes.npy', allow_pickle=True).item()


def read_dirs() -> dict:
    return np.load('C:/py/dirs.npy', allow_pickle=True).item()


ops = []
note = read_notes()
dirs = read_dirs()
funcs = {
    "sc": handle_sc,
    "p": handle_p,
    "o": handle_o,
    "w": open_web,
    "n": handle_n,
    "s": save,
}


if __name__ == "__main__":
    main()


