from graphics import Window
from card import Bingo
from server import BingoServer
from client import BingoClient
import time 
# bingo = Bingo(6)
# window = Window(bingo)

def hostGame():
    server = BingoServer(game_size=6, player_count=3)
    thread = server.initGame()
    thread.start()

    thread.join()

def Joingame():
    client=BingoClient()
    time.sleep(2)

    card=Bingo(client.game_size)   
    window=Window(card, client=client) 
    
hostGame()
