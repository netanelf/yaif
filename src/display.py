import logging
import tkinter as tk
from tkinter import ttk

from configuration import Configuration


class Display(tk.Tk):
    def __init__(self, cfg: Configuration):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._cfg = cfg

        # configure the root window
        self.title('My Awesome App')
        self.geometry('300x50')

        # label
        self.label = ttk.Label(self, text='Hello, Tkinter!')
        self.label.pack()

        # button
        self.button = ttk.Button(self, text='Click Me')
        self.button.pack()



