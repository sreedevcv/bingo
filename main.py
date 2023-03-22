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


    
hostGame()

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