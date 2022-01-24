"""Source code for the tkinter windows of gui_main.

Author: Yoshinari Motokawa <yoshinari.moto@fuji.waseda.jp>
"""

import asyncio
import threading
import tkinter
from tkinter import ttk
from typing import List

from PIL import Image, ImageOps, ImageTk
from toio_API.scenarios import SCENARIOS, make_scenario
from toio_API.utils.general import create_toios, discover_toios
from toio_API.utils.logging import initialize_logging

logger = initialize_logging(__name__)

COLORS = ["red", "blue", "green", "yellow", "orange"]


class toioDefaultWindow(tkinter.Frame):
    def __init__(self, toio_names: List[str] = None, mat_type: str = "normal"):
        if mat_type == "normal":
            self.IMAGE_HEIGHT = 425
            self.IMAGE_WIDTH = 600
            self.MAT_HEIGHT = 216
            self.MAT_WIDTH = 304
            self.MAT_HEIGHT_MIN = 142
            self.MAT_WIDTH_MIN = 98
            pil_image = Image.open("figs/normal_mat.png")

        elif mat_type == "extra":
            self.IMAGE_HEIGHT = 480
            self.IMAGE_WIDTH = 510
            self.MAT_HEIGHT = 863
            self.MAT_WIDTH = 915
            self.MAT_HEIGHT_MIN = 35
            self.MAT_WIDTH_MIN = 34
            pil_image = Image.open("figs/extra_mat.png")

        else:
            logger.warn(f"Invalid mat type is given. mat_type: {mat_type}")

            raise ValueError()

        root = tkinter.Tk()
        root.geometry(f"{self.IMAGE_WIDTH}x{self.IMAGE_HEIGHT+50}")
        root.title("Destination pointer for toio")
        super().__init__(root)
        self.stop_event = threading.Event()
        self.toio_names = toio_names + ["All"]
        self.ovals = {name: [] for name in self.toio_names}
        self.num_oval = {name: 0 for name in self.toio_names}
        self.colors = {
            name: COLORS[toio_idx] for toio_idx, name in enumerate(self.toio_names)
        }
        self.prev_event_x, self.prev_event_y = {}, {}
        self.pack()

        self.canvas = tkinter.Canvas(
            self.master, bg="white", height=self.IMAGE_HEIGHT, width=self.IMAGE_WIDTH
        )

        self.canvas.bind("<Button-1>", self.click)

        pil_image = ImageOps.pad(pil_image, (self.IMAGE_WIDTH, self.IMAGE_HEIGHT))
        self.photo_image = ImageTk.PhotoImage(image=pil_image)

        self.canvas.create_image(
            self.IMAGE_WIDTH / 2, self.IMAGE_HEIGHT / 2, image=self.photo_image
        )

        self.canvas.pack()

        self.combobox_scenario = ttk.Combobox(self.master, state="readonly", width=10)
        self.combobox_scenario["values"] = SCENARIOS
        self.combobox_scenario.set(SCENARIOS[0])
        self.combobox_scenario.pack(side="left")

        self.combobox_name = ttk.Combobox(self.master, state="readonly", width=5)
        self.combobox_name["values"] = self.toio_names
        self.combobox_name.set("All")
        self.combobox_name.pack(side="left")

        self.button_erase = tkinter.Button(self.master, text="Erase")
        self.button_erase.bind("<Button-1>", self.erase)
        self.button_erase.pack(side="left")

        self.button_erase_all = tkinter.Button(self.master, text="Erase all")
        self.button_erase_all.bind("<Button-1>", self.erase_all)
        self.button_erase_all.pack(side="left")

        self.button_run = tkinter.Button(self.master, text="Run toio")
        self.button_run.bind("<Button-1>", self.run_toio_thread)
        self.button_run.pack(side="left")

        self.button_stop = tkinter.Button(self.master, text="Stop toio")
        self.button_stop.bind("<Button-1>", self.stop_toio_thread)
        self.button_stop.pack(side="left")

        self.button_reset = tkinter.Button(self.master, text="Reset")
        self.button_reset.bind("<Button-1>", self.reset)
        self.button_reset.pack(side="left")

    def click(self, event):
        name = self.combobox_name.get()
        if self.num_oval[name] > 0:
            self.canvas.create_line(
                self.prev_event_x[name],
                self.prev_event_y[name],
                event.x,
                event.y,
                tags=f"line_{name}_{self.num_oval[name]}",
                width=2.0,
                fill="black",
            )
            self.canvas.tag_lower(
                f"line_{name}_{self.num_oval[name]}",
                f"oval_{name}_{self.num_oval[name]-1}",
            )
        self.canvas.create_oval(
            event.x - 10,
            event.y - 10,
            event.x + 10,
            event.y + 10,
            tag=f"oval_{name}_{self.num_oval[name]}",
            fill=self.colors[name],
        )
        self.canvas.create_text(
            event.x,
            event.y,
            text=str(self.num_oval[name]),
            tags=f"num_oval_{name}_{self.num_oval[name]}",
        )
        self.ovals[name].append((event.x, event.y))
        self.prev_event_x[name], self.prev_event_y[name] = event.x, event.y
        self.num_oval[name] += 1

    def erase(self, event):
        name = self.combobox_name.get()
        self.num_oval[name] = max(0, self.num_oval[name] - 1)
        if self.ovals[name]:
            self.ovals[name].pop()
            if self.num_oval[name] > 0:
                self.prev_event_x[name], self.prev_event_y[name] = self.ovals[name][-1]
        self.canvas.delete(f"oval_{name}_{self.num_oval[name]}")
        self.canvas.delete(f"num_oval_{name}_{self.num_oval[name]}")
        self.canvas.delete(f"line_{name}_{self.num_oval[name]}")

    def erase_all(self, event):
        name = self.combobox_name.get()
        for i in range(self.num_oval[name]):
            self.canvas.delete(f"oval_{name}_{i}")
            self.canvas.delete(f"num_oval_{name}_{i}")
            self.canvas.delete(f"line_{name}_{i}")
        self.num_oval[name] = 0
        self.ovals[name] = []

    def reset(self, event):
        for name in self.toio_names:
            for i in range(self.num_oval[name]):
                self.canvas.delete(f"oval_{name}_{i}")
                self.canvas.delete(f"num_oval_{name}_{i}")
                self.canvas.delete(f"line_{name}_{i}")
            self.num_oval[name] = 0
            self.ovals[name] = []

    def convert_ovals_coordination(self):
        converted_ovals = {name: [] for name in self.toio_names}
        for name in self.toio_names:
            for x, y in self.ovals[name]:
                coordinate = (
                    int((self.MAT_WIDTH * x / self.IMAGE_WIDTH) + self.MAT_WIDTH_MIN),
                    int(
                        (self.MAT_HEIGHT * y / self.IMAGE_HEIGHT) + self.MAT_HEIGHT_MIN
                    ),
                )
                converted_ovals[name].append(coordinate)
        return converted_ovals

    def run_toio(self):
        converted_ovals = self.convert_ovals_coordination()
        toio_addresses = asyncio.run(discover_toios())
        toios = create_toios(toio_addresses=toio_addresses, toio_names=self.toio_names)
        scenario = make_scenario(
            scenario_name=self.combobox_scenario.get(), toios=toios
        )
        scenario.run(**{"converted_ovals": converted_ovals, "run": self.stop_event})

    def run_toio_thread(self, event):
        self.button_run["text"] = "Running..."
        self.stop_event.clear()
        toio_thread = threading.Thread(target=self.run_toio)
        toio_thread.start()

    def stop_toio_thread(self, event):
        self.button_stop["text"] = "Stopping..."
        self.button_run["text"] = "Run toio"
        self.stop_event.set()
        self.button_stop["text"] = "Stop toio"
