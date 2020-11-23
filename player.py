import youtube_dl
import threading
import os

# player functions
def search(title, amount=10): # search for results, works
    info = youtube_dl.YoutubeDL({"quiet" : True}).extract_info(f"ytsearch{amount}:{title}", download=False, ie_key="YoutubeSearch")

    data = {}

    for entry in info["entries"]:
        data[entry["title"]] = (entry["webpage_url"], entry["thumbnails"][0]["url"]) # store title and thumbnail for display, url for downloads

    return data

# wrapper for making background tasks
class BackgroundTask(threading.Thread): 
    def __init__(self, task, args=()): # arguments must be passed like a normal thread eg (arg1, arg2,)
        threading.Thread.__init__(self)
        self.task = task # the task to be executed
        self.args = args # task arguments
        self.alive = True # flag to control waiting for feedback
        self.feedback = None # to allow feedback if function returns

    def run(self):
        self.feedback = self.task(*self.args) # initiate the function and return data
        self.alive = False # kill thread and waiting loop

# playlist class, each playlist is its own instance
class Playlist:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.songs = []

    def store(self): # create or update a playlist
        with open(os.path.join("userdata/playlists/", self.name, ".txt"), "w") as playlist:
            playlist.write(self.name + "\n")
            playlist.write(self.description + "\n")
            for song in self.songs:
                playlist.write(song + "\n")

    def load(self, playlist_name): # load a stored playlist
        files = os.listdir("userdata/playlists/")
        filename = playlist_name + ".txt"
        if filename not in files:
            return None

        with open(os.path.join("userdata/playlists/", filename), "r") as playlist:
            data = playlist.readlines()
            if len(data) < 2: # the file must have a description and title, default at least, otherwise there is an invalid format
                return False

            self.name = playlist_name
            self.description = data[0].strip("\n")
            for song in data[1:]:
                self.songs.append(song.strip("\n"))

        return True

    def delete(self): # delete a playlist
        os.remove("userdata/playlists/", self.name + ".txt")
        del self