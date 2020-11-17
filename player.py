import youtube_dl
import threading

# player functions
def search(title, amount=5): # search for results, works
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