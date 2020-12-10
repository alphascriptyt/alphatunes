import tkinter as tk
import tkinter.ttk as ttk
import sys
import os

# pages
from mainpage import MainPage

class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # colours
        self.bg_colour = "#202020"
        self.playlist_bg_colour = "#151515"
        self.taskbar_bg_colour = "#333333"
        self.sb_bar_colour = "#505050"
        self.sb_selected_colour = "#656565"
        self.dark_white_colour = "#8a8a8a"

        # fonts
        self.header_font = "Arial 32 bold"
        self.normal_font = "Arial 15" # font for playlist names and songs
        self.song_font = "Arial 12 bold"

        # images

        # basic setup
        self.default_width = 1000 # calculate this?
        self.default_height = 750 # calculate this?
        
        self.title("alphatunes")
        self.geometry(f"{self.default_width}x{self.default_height}")
        self.resizable(0, 0)
        self.minsize(self.default_width, self.default_height)

        # view mode (current frame)

        # frames, make resizable
        container = tk.Frame(self)
        container.place(x=0, y=0, width=self.default_width, height=self.default_height)
        self.frames = {"MAIN" : MainPage(container, self)}

        # call main frame
        self.frames["MAIN"].tkraise()

    def initialise_frame(self, frame_object, image=None): # for all the basic setup stuff in frames
        frame_object.place(x=0, y=0, width=self.default_width, height=self.default_height)
        frame_object.configure(bg=self.bg_colour)

        if image != None: # for making it easier to initialise a frame with a background
            background_gif = tk.PhotoImage(file=self.resource_path(image))
            background = tk.Label(frame_object, image=background_gif, borderwidth=0, highlightthickness=0)
            background.image = background_gif # keep reference to image
            background.place(x=0, y=0)

    def resource_path(self, relative_path): # copied from stackoverflow, for making the program a .exe in future
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS # PyInstaller creates a temp folder and stores path in _MEIPASS, ignore error
            
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)        
        

        

        

    
