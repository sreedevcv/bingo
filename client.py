from __future__ import annotations
import graphics 
import socket
import random
import json
from _thread import *

# from card import Bingo

# host = "10.42.0.1"
host = "127.0.0.1"
port = 5000
s_message = {"name": "", "type": "", "number": 0}
data = ""


class BingoClient:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.game_size = 0
        self.my_turn = False
        self.window = None
        self.initialize()
        
    def initialize(self):
        self.player_name = "amal" + str(random.randint(0, 10))
        data = bytes(self.player_name, "utf-8")
        self.client.sendall(data)
        data = self.client.recv(1024).decode()
        arr = data.split(" ")
        self.game_size = int(arr[0])
        # while(data=='start'):
        start_new_thread(self.client_read, ())
        # start_new_thread(client_send,(,))

    def setWindow(self, window: graphics.Window):
        self.window = window

    def client_read(self):
        while True:
            message = self.client.recv(2048).decode()
            print(message)
            response = json.loads(message)
            print(response["name"], response["type"], response["number"])

            try:
                self.window.logEvent(response)
            except AttributeError:
                print("none type error: ")


            if response["type"] == "play":
                self.my_turn = True
                if self.window != None:
                    self.window.setPlayerName("You")

            elif response["type"] == "normal":
                num = int(response["number"])
                i, j = self.window.bingo.getPointIndices(num)
                self.window.markPoint(i, j)
                self.window.setPlayerName(response["name"])


    def client_send(self, num: int):
        s_message["name"] = self.player_name
        s_message["type"] = "normal"
        s_message["number"] = num
        message = json.dumps(s_message)
        self.client.sendall(bytes(message, "utf-8"))
