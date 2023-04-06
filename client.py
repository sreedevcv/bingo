from __future__ import annotations
import graphics
import socket
import json
from _thread import *

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
        self.player_name = "amal"
        self.turn = 0
        # self.initialize()


    def initialize(self):
        data = bytes(self.player_name, "utf-8")
        self.client.sendall(data)
        data = self.client.recv(1024).decode()
        arr = data.split(" ")
        self.game_size = int(arr[0])

    def setWindow(self, window: graphics.Window):
        self.window = window

    def start_reading(self):
        start_new_thread(self.client_read, ())

    def client_read(self):
        while True:
            message = self.client.recv(2048).decode()
            print(f'>{message}<')
            server_msg = json.loads(message)

            self.window.logEvent(server_msg)
            self.turn = server_msg["turn"]

            
            if server_msg["type"] == "play" and server_msg["name"] == self.player_name:
                self.my_turn = True
                self.window.setPlayerName("You")
            elif server_msg["type"] == "play":
                self.window.setPlayerName(server_msg["name"])
            elif server_msg["type"] == "normal":
                num = int(server_msg["number"])
                i, j = self.window.card.getPointIndices(num)
                self.window.mark_point(i, j)
            elif server_msg["type"] == "finished":
                num = int(server_msg["number"])
                if num > 0:
                    i, j = self.window.card.getPointIndices(num)
                    self.window.mark_point(i, j)   
            elif server_msg["type"] == "game_over":
                self.window.setPlayerName("Over")
                break;       
            
            if server_msg["turn"] > 0:
                self.window.update_turn_field(server_msg["turn"])

    def client_send(self, msg_type:str, num: int):
        if msg_type == "normal":
            s_message["type"] = "normal"
        elif msg_type == "finished":
            s_message["type"] = "finished"

        s_message["name"] = self.player_name
        s_message["number"] = num
        s_message["turn"] = self.turn
        message = json.dumps(s_message)
        self.client.sendall(bytes(message, "utf-8"))
