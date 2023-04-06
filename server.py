import socket
import threading
import json
import time


class BingoServer:

    PORT = 5000
    # HOST = "10.42.0.1"
    HOST = "127.0.0.1"

    def __init__(self, game_size: int = 5, player_count: int = 3) -> None:
        self.player_count = player_count
        self.game_size = game_size
        self.connections = []
        self.player_names = []
        self.data_format = {"name": "", "type": "", "number": -1, "turn": 0}

    def communicate(self):
        turn = 1
        rank_list = []
        last_rank = 0
        last_rank_turn = 0
        saved_conn = [c for c in self.connections]

        while self.player_count > 1:
            for conn, name in self.connections:
                print(name)

                self.data_format["name"] = name
                self.data_format["type"] = "play"
                self.data_format["turn"] = turn
                turn_info = bytes(json.dumps(self.data_format), "utf-8")

                # Inform evertone whoser turn it is now
                for _conn, _ in self.connections:
                    _conn.sendall(turn_info)

                # Receive data from current player about their move
                recieved_data: bytes = conn.recv(1024)
                print(f"|{recieved_data}|")
                data = json.loads(recieved_data.decode())
                
                if data["type"] == "finished":
                    # Name is not already in the rank list
                    if len([1 for rl in rank_list if rl[0] == data["name"]]) == 0:
                        self.player_count -= 1
                        if data["turn"] == last_rank_turn:
                            rank_list.append((data["name"], data["turn"], last_rank))
                        else:
                            last_rank += 1
                            last_rank_turn = data["turn"]
                            rank_list.append((data["name"], data["turn"], last_rank))
                        
                        # Remove the current connection from list
                        self.connections = [x for x in self.connections if x[1] != name]
                        print(f'{name} has finished')
                        print(rank_list)

                # Inform everyone about the current player,s move
                for _conn, _ in self.connections:
                    if _conn != conn:
                        _conn.sendall(recieved_data)

                        # Receive the confirmation message
                        secondary_recv_data = _conn.recv(1024)
                        print(f'sr|{secondary_recv_data}|')
                        sec_data = json.loads(secondary_recv_data.decode())

                        # Player has finished their game so modify the sending message
                        if sec_data["type"] == "finished":
                            if data["type"] == "finished":
                                data["name"] += ' ' + sec_data["name"]
                            else :
                                data["type"] = "finished"
                                data["name"] = sec_data["name"]  
                            recieved_data = bytes(json.dumps(data), "utf-8")

                            # Name is not already in the rank list
                            if len([1 for rl in rank_list if rl[0] == sec_data["name"]]) == 0:
                                self.player_count -= 1
                                if sec_data["turn"] == last_rank_turn:
                                    rank_list.append((sec_data["name"], sec_data["turn"], last_rank))
                                else:
                                    last_rank += 1
                                    last_rank_turn = sec_data["turn"]
                                    rank_list.append((sec_data["name"], sec_data["turn"], last_rank))
                                self.connections = [x for x in self.connections if x[1] != sec_data["name"]]
                                print(f'{sec_data["name"]} has finished')
                                print(rank_list)

                                if self.player_count == 1:
                                    break

                time.sleep(0.05)
                turn += 1

        # Add the last player to rank list
        if len(self.connections) > 0:
            rank_list.append((self.connections[0][1], turn, last_rank + 1))

        print(rank_list)
        # Convert rabk list to a string
        rank_msg = ""
        for name, turn, rank in rank_list:
            s = f"{name} won {rank} place in {turn} turns\n"
            rank_msg += s

        data = {"type": "game_over", "rank_list": rank_msg, "turn": 0}
        print(data)
        # Send the rank list to everyone
        for conn, _ in saved_conn:
            conn.sendall(bytes(json.dumps(data), "utf-8"))

    def initGame(self) -> threading.Thread:
        sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind((BingoServer.HOST, BingoServer.PORT))
        sock.listen()
        print("Listening for connections...")
        # Wait for everyone to join
        for i in range(self.player_count):
            conn, addr = sock.accept()
            self.connections.append([conn,])

        print("Passing info...")
        # Give neccessary info to all clients
        for i in range(self.player_count):
            conn = self.connections[i][0]
            name = conn.recv(1024)
            conn.sendall(
                bytes(str(self.game_size) + " " + str(self.player_count), "utf-8")
            )
            self.player_names.append(name.decode())
            self.connections[i].append(name.decode())
            print(name.decode())

        return threading.Thread(target=self.communicate)
