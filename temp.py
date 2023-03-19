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
    # time.sleep(2)
    print(client.player_name)

    card = Bingo(client.game_size)
    w = Window(card, client=client, name=client.player_name)
    client.setWindow(w)
    w.start_loop()


# hostGame()
Joingame()
