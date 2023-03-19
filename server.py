import socket
import threading
import json


class BingoServer:

    PORT = 5000
    # HOST = "10.42.0.1"
    HOST = "127.0.0.1"

    def __init__(self, game_size: int = 5, player_count: int = 3) -> None:
        self.player_count = player_count
        self.game_size = game_size
        self.connections = []
        self.player_names = []
        self.data_format = {"name": "", "type": "", "number": -1}

    def communicate(self):
        while True:
            for conn, addr in self.connections:
                print(addr)
                
                self.data_format["type"] = "play"
                conn.sendall(bytes(json.dumps(self.data_format), "utf-8"))

                recieved_data: bytes = conn.recv(1024)
                data = json.loads(recieved_data.decode())

                if data["type"] == "finish":
                    self.player_count -= 1

                for conn_, _ in self.connections:
                    if conn_ != conn:
                        conn_.sendall(recieved_data)

                if self.player_count == 1:
                    break

    def initGame(self) -> threading.Thread:
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind((BingoServer.HOST, BingoServer.PORT))
        sock.listen()
        print("Listening for connections...")
        # Wait for everyone to join
        for i in range(self.player_count):
            conn, addr = sock.accept()
            self.connections.append((conn, addr))
            print(conn, addr)

        print("Passing info...")
        # Give neccessary info to all clients
        for i in range(self.player_count):
            conn = self.connections[i][0]
            name = conn.recv(1024)
            conn.sendall(bytes(str(self.game_size) + " " + str(self.player_count), "utf-8"))
            self.player_names.append(name.decode())
            print(name.decode())

        return threading.Thread(target=self.communicate)
