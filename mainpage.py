import time
import tkinter as tk
import tkinter.ttk as ttk
import sys
import os
import player
import threading
import queue

#search = player.search()

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        #intialise
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.initialise_frame(self)

        # settings
        self.current_hovered_widget = "" # store the previous colour of the element being hovered over
        self.search_results = [] # store the search results (to be displayed)

        #styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # custom scrollbars
        self.style.layout('custom.Vertical.TScrollbar', # create layout and remove the top/bottom arrows
             [('Vertical.Scrollbar.trough',
               {'children': [('Vertical.Scrollbar.thumb', 
                              {'expand': '1', 'sticky': 'nswe'})],
                'sticky': 'ns'})])
        
        self.style.layout('custom2.Vertical.TScrollbar', # create layout and remove the top/bottom arrows
             [('Vertical.Scrollbar.trough',
               {'children': [('Vertical.Scrollbar.thumb', 
                              {'expand': '1', 'sticky': 'nswe'})],
                'sticky': 'ns'})])
        
        self.style.configure("custom.Vertical.TScrollbar", gripcount=0, arrowsize=18, # custom colours (default arrowsize=15)
                background=self.controller.sb_bar_colour, darkcolor=self.controller.playlist_bg_colour, lightcolor=self.controller.playlist_bg_colour,
                troughcolor=self.controller.playlist_bg_colour, bordercolor=self.controller.playlist_bg_colour, arrowcolor=self.controller.playlist_bg_colour)

        self.style.configure("custom2.Vertical.TScrollbar", gripcount=0, arrowsize=18, # custom colours (default arrowsize=15)
                background=self.controller.sb_bar_colour, darkcolor=self.controller.bg_colour, lightcolor=self.controller.bg_colour,
                troughcolor=self.controller.bg_colour, bordercolor=self.controller.bg_colour, arrowcolor=self.controller.bg_colour)

        self.style.map("Vertical.TScrollbar", background=[("active", self.controller.sb_selected_colour)])

        # playlist section
        # playlist canvas, for the scrollbar areas (the canvas is its own frame)
        self.playlist_canvas = tk.Canvas(self, width=self.controller.default_width//5, height=self.controller.default_height, bg=self.controller.playlist_bg_colour, highlightthickness=0, borderwidth=0)
        self.playlist_canvas.place(x=18, y=0) # pushed 18px to the right for scrollbar

        # playlist area
        self.playlist_area = tk.Frame(self.playlist_canvas)
        self.playlist_area.bind('<Configure>', self.resize_playlist_canvas_scroll) # resize the canvas scrollregion each time the size of the frame changes
        self.playlist_canvas.create_window(0, 0, window=self.playlist_area) # display frame inside the canvas
        
        # scrollbars
        self.playlist_scrollbar = ttk.Scrollbar(self, command=self.playlist_canvas.yview, orient="vertical", style="custom.Vertical.TScrollbar")
        self.playlist_scrollbar.place(x=0, y=0, relheight=1, anchor='nw') # set the scrollbar to the left of the screen
        self.playlist_canvas.configure(yscrollcommand=self.playlist_scrollbar.set) 
        
        # widgets
        playlist_title = tk.Label(self.playlist_area, text="Playlists:", fg="red", bg=self.controller.playlist_bg_colour)
        playlist_title.pack()
        
        for i in range(100):
            label = tk.Label(self.playlist_canvas, text="test" + str(i), font=self.controller.normal_font, cursor="hand2", fg="red", bg=self.controller.playlist_bg_colour) # binding the widget to the canvas improves performance
            label.bind("<Enter>", lambda event, label=label: self.highlight(event, label))
            label.bind("<Leave>", lambda event, label=label: self.unhighlight(event, label))
            label.bind("<Button-1>", lambda event: print("yo"))
            self.playlist_canvas.create_window(25, i*25+25, window=label)
        
        # set scrollbar to default position at the top
        self.playlist_canvas.update_idletasks()
        self.playlist_canvas.yview_moveto(0)



        

        # main canvas
        self.main_canvas = tk.Canvas(self, width=self.controller.default_width-(self.controller.default_width//5)-36, height=self.controller.default_height, bg=self.controller.bg_colour, highlightthickness=0, borderwidth=0) # take away 36 for the scrollbars
        self.main_canvas.place(x=18+self.controller.default_width//5, y=0) # pushed 18px to the right for scrollbar

        # main area
        self.main_area = tk.Frame(self.main_canvas)
        self.main_area.bind('<Configure>', self.resize_main_canvas_scroll) # resize the canvas scrollregion each time the size of the frame changes
        self.main_canvas.create_window(18+self.controller.default_width//5, 0, window=self.main_area) # display frame inside the canvas
        
        # scrollbars
        self.main_scrollbar = ttk.Scrollbar(self, command=self.main_canvas.yview, orient="vertical", style="custom2.Vertical.TScrollbar")
        self.main_scrollbar.place(x=self.controller.default_width-18, y=0, relheight=1) # set the scrollbar to the right of the screen
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)

        # search mode
        search_label = tk.Label(self.main_canvas, text="Song Search:", fg="white", bg=self.controller.bg_colour, font=self.controller.header_font)
        self.main_canvas.create_window(self.calc_centre(self.main_canvas), 40, window=search_label)

        # search entry
        self.search_var = tk.StringVar()
        self.search_var.set("Search")
        self.search_entry = tk.Entry(self.main_canvas, textvariable=self.search_var, cursor="xterm", font=self.controller.normal_font)
        self.search_entry.bind("<Button-1>", lambda event: self.search_var.set(""))
        self.main_canvas.create_window(self.calc_centre(self.main_canvas), 100, window=self.search_entry)

        # search button
        self.search_button = tk.Button(self.main_canvas, text="Search", font=self.controller.normal_font, cursor="hand2", fg="green", bg=self.controller.playlist_bg_colour, command=lambda: self.song_search(self.search_var.get()))
        self.main_canvas.create_window(self.calc_centre(self.main_canvas), 150, window=self.search_button)
        
        # set scrollbar to default position at the top
        self.main_canvas.update_idletasks()
        self.main_canvas.yview_moveto(0)

    def song_search(self, title):
        if title.strip(" ") != "" and title.strip(" ") != "Search":
            task = player.BackgroundTask(player.search, args=(title,))
            task.start()

            while task.alive: # wait for feedback
                self.controller.update()
                time.sleep(0.01) # let CPU rest

            print(task.feedback)

            
            

            
            
    def calc_centre(self, canvas):
        canvas.update()
        offset = canvas.winfo_width()//2 # get the midpoint of the screen

        return offset

    # resize functions
    def resize_playlist_canvas_scroll(self, event):
        self.playlist_canvas.configure(scrollregion=self.playlist_canvas.bbox('all'))

    def resize_main_canvas_scroll(self, event):
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox('all'))

    # functions for highlighting animation
    def highlight(self, event, label):
        self.current_hovered_widget = label["fg"]
        label.configure(fg="white")

    def unhighlight(self, event, label):
        label.configure(fg=self.current_hovered_widget)
