from __future__ import annotations
import client
import server
import tkinter as tk
from card import Bingo
import _thread
# from tkinter import ttk


class Window:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Bingo")
        self.root.geometry("600x600")
        self.labels = []
        self.box_width = 75
        self.padding = 5
        self.points_won = 0

        self.create_start_page()
        self.root.mainloop()

    def create_start_page(self):
        self.start_page = tk.Frame(
            master=self.root, background="green", height=600, width=600
        )
        start_btn = tk.Button(
            master=self.start_page,
            text="Start",
            command=self.goto_options_frame,
        )
        start_btn.pack(anchor="center", expand=True)
        self.start_page.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

    def create_info_label(self, game_frame: tk.Frame) -> tk.Frame:
        info_frame = tk.Frame(master=game_frame, relief=tk.RAISED)

        self.info_label = tk.Label(
            master=info_frame,
            height=2,
            text="Player:",
            justify=tk.LEFT,
            relief=tk.RAISED,
        )
        self.points_won_field = tk.Label(
            master=info_frame,
            height=2,
            text="Points: 0",
            justify=tk.LEFT,
            relief=tk.RAISED,
        )
        self.turn_field = tk.Label(
            master=info_frame,
            height=2,
            text="Turn: 0",
            justify=tk.LEFT,
            relief=tk.RAISED,
        )
        self.info_label.pack(
            side=tk.LEFT, fill=tk.X, padx=self.padding, pady=self.padding, expand=True
        )
        self.points_won_field.pack(
            side=tk.LEFT, fill=tk.X, padx=self.padding, pady=self.padding, expand=True
        )
        self.turn_field.pack(
            side=tk.LEFT, fill=tk.X, padx=self.padding, pady=self.padding, expand=True
        )
        return info_frame

    def create_bingo_grid(self, game_frame: tk.Frame) -> tk.Frame:
        grid_frame = tk.Frame(master=game_frame)

        for i in range(self.size):
            # Make the grid responsive
            grid_frame.rowconfigure(i, weight=1, minsize=self.box_width)
            grid_frame.columnconfigure(i, weight=1, minsize=self.box_width)
            temp = []
            for j in range(self.size):
                frame = tk.Frame(master=grid_frame, relief=tk.RAISED, borderwidth=1)

                # sticky='nesw' since individual frames have
                # to expand to all directions when resized
                frame.grid(
                    row=i, column=j, padx=self.padding, pady=self.padding, sticky="nesw"
                )
                label = tk.Label(
                    master=frame, text=f"{self.bingo_matrix[i][j][0]}", name=f"{i} {j}"
                )

                label.bind("<Button-1>", self.handle_click_on_number)
                temp.append(label)

                # expand=True makes the text centered inside the label
                # fill makes it fill the frame excluding the padding
                label.pack(
                    padx=self.padding, pady=self.padding, expand=True, fill=tk.BOTH
                )
            self.labels.append(temp)

        return grid_frame

    def create_log_feild(self, game_frame: tk.Frame) -> tk.Frame:
        # Create a scrollbar
        scroll_frame = tk.Frame(master=game_frame)
        v_scrollbar = tk.Scrollbar(scroll_frame)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text = tk.Text(
            master=scroll_frame,
            width=self.size * (self.box_width + self.padding) // 6,
            height=5,
            wrap=None,
            yscrollcommand=v_scrollbar.set,
        )

        self.text.pack(side=tk.TOP, fill=tk.X)
        v_scrollbar.config(command=self.text.yview)
        return scroll_frame

    def create_options_frame(self):
        self.option_frame = tk.Frame(master=self.root, background="blue")

        # create a frame for holding name_label and name_entry
        name_frame = tk.Frame(master=self.option_frame)
        name_label = tk.Label(master=name_frame, text="Name")
        name_entry = tk.Entry(master=name_frame)
        name_label.pack(fill=tk.X, side=tk.LEFT, expand=True)
        name_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)
        name_frame.pack()

        # Button for joining game
        join_btn_frame = tk.Frame(master=self.option_frame)
        join_btn = tk.Button(
            master=join_btn_frame,
            text="Join Game",
            command=lambda: self.start_client(
                name_entry,
                join_btn,
            ),
        )
        join_btn.pack(anchor="center", side=tk.TOP)
        join_btn_frame.pack(fill=tk.X, anchor="center", pady=20)

        # create a frame for holding game_size_label and game_size_entry
        game_size_frame = tk.Frame(master=self.option_frame)
        game_size_label = tk.Label(master=game_size_frame, text="game_size")
        game_size_entry = tk.Entry(master=game_size_frame)
        game_size_label.pack(fill=tk.X, side=tk.LEFT, expand=True)
        game_size_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)
        game_size_frame.pack(fill=tk.X, anchor="center", pady=20)

        # create a frame for holding player_count_label and player_count_entry
        player_count_frame = tk.Frame(master=self.option_frame)
        player_count_label = tk.Label(master=player_count_frame, text="Player Count")
        player_count_entry = tk.Entry(master=player_count_frame)
        player_count_label.pack(fill=tk.X, side=tk.LEFT, expand=True)
        player_count_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)
        player_count_frame.pack(fill=tk.X, anchor="center", pady=20)

        # Button for joining game
        start_server_frame = tk.Frame(master=self.option_frame)
        start_server_btn = tk.Button(
            master=start_server_frame,
            text="Start Server",
            command=lambda: _thread.start_new_thread(
                self.create_server,
                (game_size_entry, player_count_entry, start_server_btn),
            ),
        )
        start_server_btn.pack(anchor="center", side=tk.TOP)
        start_server_frame.pack(fill=tk.X, anchor="center", pady=20)

        self.option_frame.pack(expand=True)
        print("options frame packed")

    def goto_game_frame(self):
        game_frame = tk.Frame(master=self.root)
        info_frame = self.create_info_label(game_frame)
        grid_frame = self.create_bingo_grid(game_frame)
        scroll_frame = self.create_log_feild(game_frame)

        info_frame.pack(side=tk.TOP, fill=tk.X)
        grid_frame.pack(fill=tk.BOTH, expand=True)
        scroll_frame.pack()

        self.option_frame.destroy()
        game_frame.pack(fill=tk.BOTH, expand=True)

        # return game_frame

    def goto_options_frame(self):
        self.start_page.destroy()
        self.create_options_frame()
        print("options frame created")

    def start_client(self, name_entry, join_btn):
        player_name = name_entry.get()
        join_btn.config(text="Joining")
        self.client = client.BingoClient()

        if player_name != None:
            self.client.player_name = player_name

        self.client.initialize()
        card = Bingo(self.client.game_size)
        self.bingo_matrix = card.bingo_matrix
        self.card = card
        self.size = card.row

        self.goto_game_frame()
        self.client.setWindow(self)
        self.client.start_reading()
        # self.start_loop()

    def create_server(self, game_size_entry, player_count_entry, start_server_btn):
        _thread.start_new_thread(
            self.start_server,
            (
                game_size_entry,
                player_count_entry,
                start_server_btn,
            ),
        )

    def start_server(self, game_size_entry, player_count_entry, start_server_btn):
        data = player_count_entry.get()
        start_server_btn.config(text="Running...")
        pcount = 1

        try:
            pcount = int(data)
            if pcount < 1:
                raise ValueError
        except ValueError:
            pcount = 1

        data = game_size_entry.get()
        gcount = 4
        try:
            gcount = int(data)
            if gcount < 4:
                raise ValueError
        except ValueError:
            gcount = 4

        bingo_server = server.BingoServer(game_size=gcount, player_count=pcount)
        server_thread = bingo_server.initGame()
        server_thread.start()

    def handle_click_on_number(self, event: tk.Event) -> None:
        label = event.widget
        indices = list(map(lambda x: int(x), label._name.split(" ")))

        if not self.bingo_matrix[indices[0]][indices[1]][1] and self.client.my_turn:
            self.client.my_turn = False
            label.config(bg="yellow")
            self.bingo_matrix[indices[0]][indices[1]][1] = True
            self.card.marked_entry(indices[0], indices[1])

            self.points_won = 0
            for i in range(2 * self.size + 2):
                if self.card.marked_ele[i] == self.size:
                    self.points_won += 1
                    self.mark_line(i)

            self.client.client_send(label.cget("text"))
            self.logEvent({"type": "my_move", "number": label.cget("text")})
            self.update_points_earned()
            self.card.analyse()

    def mark_line(self, position: int) -> None:
        if position < self.size:
            for label in self.labels[position]:
                label.config(bg="red")
        elif position < 2 * self.size:
            for j in range(self.size):
                self.labels[j][position - self.size].config(bg="red")
        elif position == 2 * self.size:
            for i in range(self.size):
                self.labels[i][i].config(bg="red")
        else:
            for i in range(self.size):
                self.labels[i][self.size - 1 - i].config(bg="red")

    def mark_point(self, i: int, j: int) -> None:
        if not self.bingo_matrix[i][j][1]:
            self.labels[i][j].config(bg="yellow")
            self.bingo_matrix[i][j][1] = True
            self.card.marked_entry(i, j)
            self.points_won = 0

            for i in range(2 * self.size + 2):
                if self.card.marked_ele[i] == self.size:
                    self.mark_line(i)
                    self.points_won += 1

            self.update_points_earned()
            self.card.analyse()

    def logEvent(self, data: dict):
        string = ""
        if data["type"] == "normal":
            string = f"{data['name']} marked {data['number']}\n"
        elif data["type"] == "my_move":
            string = f"You marked {data['number']}\n"

        self.text.insert(tk.END, string)
        self.text.see(tk.END)

    def update_points_earned(self):
        if self.points_won <= self.size:
            self.points_won_field.configure(text=f"Points: {self.points_won}")

    def setPlayerName(self, name: str):
        self.info_label.config(text=f"Player: {name}")

    def update_turn_field(self, turn):
        self.turn_field.config(text=f"Turn: {turn}")

    def start_loop(self):
        self.root.mainloop()
