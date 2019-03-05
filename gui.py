#!/usr/bin/env python3
from client import Client
from tkinter import *

root = Tk()

location_label = Label(root, text="Enter Location")
location_entry = Entry(root)
submit_button = Button(root, text="submit", bg="red")

location_label.grid(row=0, column=0)
location_entry.grid(row=0, column=1)
submit_button.grid(row=1, columnspan=2)

root.mainloop()
