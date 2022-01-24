"""Source code for the GUI main entry.

Author: Yoshinari Motokawa <yoshinari.moto@fuji.waseda.jp>
"""

from toio_API.utils.tkinter_setup import toioDefaultWindow

if __name__ == "__main__":
    app = toioDefaultWindow(toio_names=["Yoshi", "Moto"])
    app.mainloop()
