import tkinter
from PIL import Image, ImageTk, ImageOps

IMAGE_HEIGHT = 425
IMAGE_WIDTH = 600


class MyApp1(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.num_oval = 0
        self.ovals = []
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

        self.button = tkinter.Button(self.master, text='Erase all')
        self.button.bind("<Button-1>", self.erase_all)
        self.button.pack(side='left')

        self.button = tkinter.Button(self.master, text='Print coordinates')
        self.button.bind("<Button-1>", self.print_ovals)
        self.button.pack(side='left')

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

    def print_ovals(self, event):
        converted_ovals = []
        for x, y in self.ovals:
            coordinate = (int((304 * x / IMAGE_WIDTH) + 98), int((216 * y / IMAGE_HEIGHT) + 142))
            converted_ovals.append(coordinate)
        print(converted_ovals)


if __name__ == '__main__':
    root = tkinter.Tk()
    root.geometry(f"{IMAGE_WIDTH}x{IMAGE_HEIGHT+50}")
    root.title("Destination pointer for toio")
    app = MyApp1(master=root)
    app.mainloop()
