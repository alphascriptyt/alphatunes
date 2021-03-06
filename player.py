import youtube_dl
import threading
import os

# player functions
def search(title, amount=10): # search for results, works
    info = youtube_dl.YoutubeDL({"quiet" : True}).extract_info(f"ytsearch{amount}:{title}", download=False, ie_key="YoutubeSearch")

    data = {}

    for entry in info["entries"]:
        data[entry["title"]] = (entry["webpage_url"], entry["thumbnails"][0]["url"]) # store title and thumbnail for display, url for downloads, keep this format for storing the songs in playlist too

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
    def __init__(self): # create function done in initialiser, basically use preset values
        self.directory = "/userdata/playlists"

        # playlist data
        self.name = f"Playlist {}"
        self.description = "..."
        self.songs = {}

    def validate_dirs(self):
        if not os.path.isdir(self.directory): # create folders if not found, check each time playlist is stored
            os.makedirs(self.directory)
            return True # validated

        return None # nothing done

    def store(self): # create or update a playlist
        validate_dirs()
        with open(os.path.join(self.directory, self.name, ".txt"), "w") as playlist:
            playlist.write(self.name + "\n")
            playlist.write(self.description + "\n")
            
            for song in self.songs:
                title = song
                url, thumbnail_url = self.songs[title]
                playlist.write(title + "\\" + url + "\\" + thumbnail_url + "\n")

            return True

    def load(self, playlist_name): # load a stored playlist
        if validate_dirs():
            return None # had to create file, there are no stored playlists
        
        files = os.listdir(self.directory)
        filename = playlist_name + ".txt"
        if filename not in files: # couldn't find file
            return None

        with open(os.path.join(self.directory, filename), "r") as playlist:
            data = playlist.readlines()
            if len(data) < 2: # the file must have a description and title, default at least, otherwise it is of an invalid format
                return False

            self.name = playlist_name
            self.description = data[0].strip("\n")

            for song in data[1:]:
                try:
                    parts = song.strip("\n").split("\\")
                    title = parts[0]
                    data = (parts[1], parts[2]) # make this metadata, include author, publish date?
                    self.songs[title] = data

                except IndexError: # invalid data format
                    return False

        return True
    
    def delete(self): # delete a playlist
        os.remove(self.directory, self.name + ".txt")
        del self
