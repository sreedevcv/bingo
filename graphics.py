# import random
# import threading
# import time
import tkinter as tk
from tkinter import ttk
from card import Bingo

from client import BingoClient


class Window:
    def __init__(self, bingo: Bingo, client: BingoClient, name) -> None:
        self.root = tk.Tk(className=name)
        self.bingo = bingo
        self.size = bingo.row
        self.bingo_matrix = bingo.bingo_matrix
        self.labels = []
        self.client = client
        self.box_width = 75
        self.padding = 5
        self.points_won = 0
        self.text = None
        # self.window.wm_/

        self.createInfoLabel()
        self.createBingoGrid()
        self.createLogFeild()

    def handleClick(self, event: tk.Event) -> None:
        label = event.widget
        indices = list(map(lambda x: int(x), label._name.split(" ")))

        if not self.bingo_matrix[indices[0]][indices[1]][1] and self.client.my_turn:
            # print(label.cget("text"), label._name)
            self.client.my_turn = False
            label.config(bg="yellow")
            self.bingo_matrix[indices[0]][indices[1]][1] = True
            self.bingo.marked_entry(indices[0], indices[1])

            self.points_won = 0
            for i in range(2 * self.size + 2):
                if self.bingo.marked_ele[i] == self.size:
                    self.points_won += 1
                    self.markLine(i)

            self.client.client_send(label.cget("text"))
            self.logEvent({"type":"my_move", "number":label.cget("text")})
            self.update_points_earned()
            self.bingo.analyse()

    def markLine(self, position: int) -> None:
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

    def markPoint(self, i: int, j: int) -> None:
        if not self.bingo_matrix[i][j][1]:
            self.labels[i][j].config(bg="yellow")
            self.bingo_matrix[i][j][1] = True
            self.bingo.marked_entry(i, j)
            self.points_won = 0

            for i in range(2 * self.size + 2):
                if self.bingo.marked_ele[i] == self.size:
                    self.markLine(i)
                    self.points_won += 1

            self.update_points_earned()
            self.bingo.analyse()

    def createBingoGrid(self) -> None:
        grid_frame = tk.Frame()

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

                label.bind("<Button-1>", self.handleClick)
                temp.append(label)

                # expand=True makes the text centered inside the label
                # fill makes it fill the frame excluding the padding
                label.pack(
                    padx=self.padding, pady=self.padding, expand=True, fill=tk.BOTH
                )
            self.labels.append(temp)

        # fill=tk.BOTH makes the grid_frame expand
        # in X and Y axis when window is resized
        grid_frame.pack(fill=tk.BOTH, expand=True)

    def createLogFeild(self):
        # Create a scrollbar
        scroll_frame = tk.Frame(master=self.root)
        v_scrollbar = tk.Scrollbar(scroll_frame)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # print("length", self.size * (self.box_width + self.padding))
        self.text = tk.Text(
            master=scroll_frame,
            width=self.size * (self.box_width + self.padding) // 6,
            height=5,
            wrap=None,
            yscrollcommand=v_scrollbar.set,
        )

        self.text.pack(side=tk.TOP, fill=tk.X)
        v_scrollbar.config(command=self.text.yview)
        
        scroll_frame.pack()

    def createInfoLabel(self):
        info_frame = tk.Frame(master=self.root, relief=tk.RAISED)

        self.info_label = tk.Label(
            master=info_frame,
            # width=self.size * (self.box_width + self.padding) // 6,
            height=2,
            text="Player:",
            justify=tk.LEFT,
            relief=tk.RAISED,
        )
        self.points_won_field = tk.Label(
            master=info_frame,
            # width=self.size * (self.box_width + self.padding) // 6,
            height=2,
            text="Points: 0",
            justify=tk.LEFT,
            relief=tk.RAISED,
        )
        self.info_label.pack(side=tk.LEFT, fill=tk.X, padx=self.padding, pady=self.padding, expand=True)
        self.points_won_field.pack(side=tk.LEFT, fill=tk.X, padx=self.padding, pady=self.padding, expand=True)
        info_frame.pack(side=tk.TOP, fill=tk.X)


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
            self.points_won_field.configure(text = f'Points: {self.points_won}')
        
        
    
    def setPlayerName(self, name:str):
        # self.info_label.config(text=f'Player: {name}')
        pass

    def start_loop(self):
        self.root.mainloop()


# a = Window(Bingo(5))
# b = App(a)
# b.start()
# a.root.mainloop()


# threading.Thread.join(b)
