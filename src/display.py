import logging
import tkinter as tk
from tkinter import ttk, Frame
from PIL import Image as PilImage, ImageTk, ImageFont, ImageDraw
import os

from configuration import Configuration
from image_list import ImageList
from data_structs.image import Image
from screen_controller_base import ScreenControllerBase


class Display(tk.Tk):
    def __init__(self, cfg: Configuration, image_list: ImageList, screen_controller: ScreenControllerBase):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._cfg = cfg
        self._image_list = image_list
        self._screen_controller = screen_controller
        self._screen_controller.turn_on_screen()

        self._first_image_shown = False
        self._screen_ratio = self._cfg.screen_size[0] / self._cfg.screen_size[1]
        self._after_handler = None
        self._create_gui()
        self._show_next_image()

    def _create_gui(self):
        self.title('YAIF (YetAnotherImageFrame)')
        if self._cfg.run_true_fullscreen:
            self.attributes('-fullscreen', True)  # really full screen
        else:
            self.attributes('-zoomed', True)  # almost fullscreen

        self._view_window = tk.Canvas(self, width=self._cfg.screen_size[1], height=self._cfg.screen_size[0])
        self._view_window.pack(fill=tk.BOTH, expand=True)

        #self._create_side_panel()

    def _create_side_panel(self):
        self._side_panel = Frame(self._view_window)

        self._exit_b = ttk.Button(self._side_panel, text="exit", command=self._exit)
        self._exit_b.pack(side=tk.TOP, fill=tk.BOTH, expand=False, pady=20)

        self._back_b = tk.Button(self._side_panel, text="back", command=self._back_one_image)
        self._back_b.pack(side=tk.TOP, fill=tk.BOTH, expand=False, pady=20)

        self._next_b = tk.Button(self._side_panel, text="next", command=self._show_next_image)
        self._next_b.pack(side=tk.TOP, fill=tk.BOTH, expand=False, pady=20)

        self._side_panel_canvas = self._view_window.create_window(
            0,
            0,
            anchor="nw",
            window=self._side_panel,
        )

    def _back_one_image(self, event=None):
        image = self._image_list.get_last_shown_image()
        self._show_image(image)

    def _show_next_image(self):
        image = self._image_list.get_next_image()
        self._show_image(image)
        if self._after_handler is not None:
            self.after_cancel(self._after_handler)
        self._after_handler = self.after(self._cfg.display_time_sec * 1000, self._show_next_image)

    def _exit(self):
        self.destroy()

    def _show_image(self, image: Image):
        self._logger.debug(f'trying to show image: {image.image_path}')
        im = PilImage.open(image.image_path)
        im = self._scale_image(im)
        im = self._add_annotations(im, image)
        im = ImageTk.PhotoImage(im)
        self._view_window.image = im
        self._saved_im = im
        if not self._first_image_shown:
            self._image_container = self._view_window.create_image(
                int(self._cfg.screen_size[1] / 2), int(self._cfg.screen_size[0] / 2),
                anchor=tk.CENTER,
                image=im,
                tags="bg_img")
            self._first_image_shown = True
        else:
            self._view_window.itemconfig(self._image_container, image=im)

    def _add_annotations(self, im: PilImage, image_data: Image):
        font = ImageFont.truetype("../assets/FreeSansBold.ttf", 24)
        draw = ImageDraw.Draw(im)
        draw.text((10, 10), f"{os.path.basename(image_data.image_path)}", (255, 0, 0), font=font)
        return im

    def _scale_image(self, im: PilImage) -> PilImage:
        w, h = im.size
        im_ratio = h / w
        if im_ratio < self._screen_ratio:
            im = im.resize((self._cfg.screen_size[1], int(self._cfg.screen_size[1] * im_ratio)), PilImage.ANTIALIAS)
        else:
            im = im.resize((int(self._cfg.screen_size[0] / im_ratio), self._cfg.screen_size[0]), PilImage.ANTIALIAS)
        return im
