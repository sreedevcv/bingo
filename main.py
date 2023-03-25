from graphics import Window
from card import Bingo
from server import BingoServer
from client import BingoClient
import time 


def hostGame():
    server = BingoServer(game_size=5, player_count=2)
    thread = server.initGame()
    thread.start()

    thread.join()


    
# hostGame()

# from tkinter import *
# from PIL import Image, ImageTk

# ws = Tk()
# ws.title('PythonGuides')


# img = PhotoImage(file='data/logo.png')
# Label(
#     ws,
#     image=img,
#     anchor="center"
# ).pack()

# ws.mainloop()

# class Window:
#     def __init__(self) -> None:
#         self.root = Tk()
#         self.root.title("Bingo")
#         # self.root.geometry("600x600")

#         self.create_start_page()

#     def create_start_page(self):
#         self.start_page = Frame(
#             master=self.root, 
#         )

#         logo_img = PhotoImage(file='data/logo.png')
#         logo_label = Label(master=self.start_page, image=logo_img, anchor='center')

#         start_btn = Button(
#             master=self.start_page,
#             text="Start",
#         )

#         logo_label.pack()
#         # start_btn.pack(anchor="center", expand=True)
#         # self.start_page.pack(fill=BOTH, expand=True, side=TOP)
#         self.start_page.pack()
#         self.root.mainloop()

    
# a = Window()


import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

def popup_bonus():
    win = tk.Toplevel()
    win.wm_title("Window")

    l = tk.Label(win, text="Input")
    l.grid(row=0, column=0)

    b = ttk.Button(win, text="Okay", command=win.destroy)
    b.grid(row=1, column=0)

def popup_showinfo():
    showinfo("Window", "Hello World!")

class Application(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack()

        self.button_bonus = ttk.Button(self, text="Bonuses", command=popup_bonus)
        self.button_bonus.pack()

        self.button_showinfo = ttk.Button(self, text="Show Info", command=popup_showinfo)
        self.button_showinfo.pack()

root = tk.Tk()

app = Application(root)

root.mainloop()
