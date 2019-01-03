import os
from tkinter import *

from PIL import ImageTk


def callback(event):
    print("clicked at", event.x, event.y)
    (pos_x, pos_y) = canvas.coords(time_scroller)
    canvas.move(time_scroller, event.x - pos_x, event.y - pos_y)


def drag(event):
    print("drag at", event.x, event.y)
    (pos_x, pos_y) = canvas.coords(time_scroller)
    canvas.move(time_scroller, event.x - pos_x, event.y - pos_y)


root = Tk()
root.resizable(0, 0)

canvas = Canvas(root, width=1440, height=400, bg='blue', borderwidth=0,
                highlightthickness=0)
canvas.bind("<Button-1>", callback)
canvas.bind("<B1-Motion>", drag)
canvas.pack(expand=1, fill=BOTH)

image = ImageTk.PhotoImage(
    file="." + os.path.sep + "gui-all-data-with-minimap.png")
canvas.create_image(0, 0, image=image, anchor=NW)

time_image = ImageTk.PhotoImage(file="." + os.path.sep + "gui-bits-time.png")
time_scroller = canvas.create_image(0, 0, image=time_image, anchor=CENTER)

root.mainloop()
