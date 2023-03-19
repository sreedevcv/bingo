import socket
import threading
import json

class BingoServer:

    PORT = 5000
    HOST = "10.42.0.1"

    def __init__(self, game_size: int = 5, player_count: int = 3) -> None:
        self.player_count = player_count
        self.game_size = game_size
        self.connections = []
        self.player_names = []

    def communicate(self):
        while True:
            for conn, addr in self.connections:
                print(addr)
                conn.sendall(bytes('START'))
                data = conn.recv(1024)

                for conn_, addr_ in self.connections:
                    if conn_ != conn:
                        if "FINISHED" in data.decode():
                            conn_.sendall(bytes(data.decode() + " " + addr_))
                            self.player_count -= 1
                        else:
                            conn_.sendall(data)

                if self.player_count == 1:
                    break

    def initGame(self) -> threading.Thread:
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        sock.bind((BingoServer.HOST, BingoServer.PORT))
        sock.listen()

        # Wait for everyone to join
        for i in range(self.player_count):
            conn, addr = sock.accept()
            self.connections.append((conn, addr))
            print(conn, addr)

        # Give neccessary info to all clients
        for i in range(self.player_count):
            conn = self.connections[i][1]
            name = conn.recv(1024)
            conn.sendall(bytes(self.game_size + " " + self.player_count))
            self.player_names.append(name.decode())
            print(name.decode())

        return threading.Thread(target=self.communicate)
