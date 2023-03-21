from graphics import Window
from card import Bingo
from server import BingoServer
from client import BingoClient
import time 
# bingo = Bingo(6)
# window = Window(bingo)

def hostGame():
    server = BingoServer(game_size=5, player_count=1)
    thread = server.initGame()
    thread.start()

    thread.join()


    
# hostGame()

int('aff')