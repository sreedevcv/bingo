from graphics import Window
from card import Bingo
from server import BingoServer
from client import BingoClient
import time

# bingo = Bingo(6)
# window = Window(bingo)


def hostGame():
    server = BingoServer(game_size=5, player_count=2)
    thread = server.initGame()
    thread.start()

    thread.join()


def Joingame():
    client = BingoClient()
    print(client.player_name)
    card = Bingo(client.game_size)
    w = Window(card, client=client, name=client.player_name)
    client.setWindow(w)
    client.start_reading()
    w.start_loop()


# hostGame()
# Joingame()
a = Window()

# from tkinter import *
# from PIL import Image, ImageTk

# class test:
#     def __init__(self) -> None:
        
#         self.root = Tk()
#         self.root.title('PythonGuides')
#         self.create_frame()

#     def create_frame(self):
#         self.temp = Frame(self.root)

#         img = PhotoImage(file='data/logo.png')
#         lab = Label(
#             self.temp,
#             image=img,
#             anchor="center"
#         )
#         lab.pack()
#         self.temp.pack()
#         self.root.mainloop()


# a = test()