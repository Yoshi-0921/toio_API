import tkinter
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
from toio_API.scenarios import SCENARIOS
import asyncio
from toio_API.scenarios import make_scenario
from toio_API.utils.general import create_toios, discover_toios
import threading


IMAGE_HEIGHT = 425
IMAGE_WIDTH = 600


class toioHandler(tkinter.Frame):
    def __init__(self, toio_names=None):
        root = tkinter.Tk()
        root.geometry(f"{IMAGE_WIDTH}x{IMAGE_HEIGHT+50}")
        root.title("Destination pointer for toio")
        super().__init__(root)
        self.num_oval = 0
        self.ovals = []
        self.stop_event = threading.Event()
        self.toio_names = toio_names
        self.pack()

        self.canvas = tkinter.Canvas(self.master, bg="white", height=IMAGE_HEIGHT, width=IMAGE_WIDTH)

        self.canvas.bind('<Button-1>', self.click)

        pil_image = Image.open('figs/normal_mat.png')

        pil_image = ImageOps.pad(pil_image, (IMAGE_WIDTH, IMAGE_HEIGHT))
        self.photo_image = ImageTk.PhotoImage(image=pil_image)

        self.canvas.create_image(
            IMAGE_WIDTH / 2,
            IMAGE_HEIGHT / 2,
            image=self.photo_image
        )

        self.canvas.pack()

        self.combobox = ttk.Combobox(self.master, state="readonly")
        self.combobox["values"] = SCENARIOS
        self.combobox.set(SCENARIOS[0])
        self.combobox.pack(side='left')

        self.button_erase = tkinter.Button(self.master, text='Erase all')
        self.button_erase.bind("<Button-1>", self.erase_all)
        self.button_erase.pack(side='left')

        self.button_run = tkinter.Button(self.master, text='Run toio')
        self.button_run.bind("<Button-1>", self.run_toio_thread)
        self.button_run.pack(side='left')

        self.button_stop = tkinter.Button(self.master, text='Stop toio')
        self.button_stop.bind("<Button-1>", self.stop_toio_thread)
        self.button_stop.pack(side='left')

    def click(self, event):
        self.num_oval += 1
        if self.num_oval > 1:
            self.canvas.create_line(self.prev_event_x, self.prev_event_y, event.x, event.y, tags="line", width=2.0, fill="blue")
            self.canvas.tag_lower('line', 'oval')
        self.canvas.create_oval(event.x - 10, event.y - 10, event.x + 10, event.y + 10, tag="oval", fill='red')
        self.canvas.create_text(event.x, event.y, text=str(self.num_oval), tags="num_oval")
        self.ovals.append((event.x, event.y))
        self.prev_event_x, self.prev_event_y = event.x, event.y

    def erase_all(self, event):
        self.canvas.delete("oval")
        self.canvas.delete("num_oval")
        self.canvas.delete("line")
        self.num_oval = 0
        self.ovals = []

    def convert_ovals_coordination(self):
        converted_ovals = []
        for x, y in self.ovals:
            coordinate = (int((304 * x / IMAGE_WIDTH) + 98), int((216 * y / IMAGE_HEIGHT) + 142))
            converted_ovals.append(coordinate)
        return converted_ovals

    def run_toio(self):
        converted_ovals = self.convert_ovals_coordination()
        toio_addresses = asyncio.run(discover_toios())
        toios = create_toios(toio_addresses=toio_addresses, toio_names=self.toio_names)
        scenario = make_scenario(scenario_name=self.combobox.get(), toios=toios)
        scenario.run(**{'converted_ovals': converted_ovals, 'run': self.stop_event})

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
