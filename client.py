import socket
import threading
import json
from _thread import *

host = socket.gethostname()
port = 2121
s_message = {"name": "", "type": "", "number": 0}
data = ""


class Client:
    def initialize(self):
        self.player_name = "amal"
        data = bytes(player_name, "utf-8")
        self.client.sendall(data)
        data = self.client.recv(1024).decode()
        arr = data.split(" ")
        self.game_size = int(arr[0])
        # while(data=='start'):
        start_new_thread(client_read, ())
        # start_new_thread(client_send,(,))

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.game_size = 0
        initialize()

    def client_read(self):
        message = self.client.recv(1024).decode()
        response = json.loads(message)
        print(response["name"], response["type"], response["number"])

    def client_send(self, num: int):
        s_message["name"] = self.player_name
        s_message["type"] = "normal"
        s_message["number"] = num
        message = json.dumps(s_message)
        self.client.sendall(message)
