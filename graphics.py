import random
import threading
import time
import tkinter as tk
from card import Bingo

from client import BingoClient


class Window:
    def __init__(self, bingo: Bingo, client: BingoClient, name) -> None:
        self.root = tk.Tk(className=name)
        self.bingo = bingo
        self.size = bingo.row
        self.points = 0
        self.bingo_matrix = bingo.bingo_matrix
        self.labels = []
        self.client = client
        self.box_width = 75
        self.padding = 5
        self.text = None
        # self.window.wm_/
        self.draw()

    def handleClick(self, event: tk.Event) -> None:
        label = event.widget
        indices = list(map(lambda x: int(x), label._name.split(" ")))

        if not self.bingo_matrix[indices[0]][indices[1]][1] and self.client.my_turn:
            # print(label.cget("text"), label._name)
            self.client.my_turn = False
            label.config(bg="yellow")
            self.bingo_matrix[indices[0]][indices[1]][1] = True
            self.bingo.marked_entry(indices[0], indices[1])

            for i in range(2 * self.size + 2):
                if self.bingo.marked_ele[i] == self.size:
                    self.markLine(i)

            self.client.client_send(label.cget("text"))
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

            for i in range(2 * self.size + 2):
                if self.bingo.marked_ele[i] == self.size:
                    self.markLine(i)
            self.bingo.analyse()

    def draw(self) -> None:
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
                frame.grid(row=i, column=j, padx=self.padding, pady=self.padding, sticky="nesw")
                label = tk.Label(
                    master=frame, text=f"{self.bingo_matrix[i][j][0]}", name=f"{i} {j}"
                )

                label.bind("<Button-1>", self.handleClick)
                temp.append(label)

                # expand=True makes the text centered inside the label
                # fill makes it fill the frame excluding the padding
                label.pack(padx=self.padding, pady=self.padding, expand=True, fill=tk.BOTH)
            self.labels.append(temp)

        # fill=tk.BOTH makes the grid_frame expand
        # in X and Y axis when window is resized
        grid_frame.pack(fill=tk.BOTH, expand=True)

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
    
    def logEvent(self, data: dict):
        string = ""
        if data["type"] == "normal":
            string = f"{data['name']} marked {data['number']}\n"

        self.text.insert(tk.END, string)



    def start_loop(self):
        self.root.mainloop()




# a = Window(Bingo(5))
# b = App(a)
# b.start()
# a.root.mainloop()


# threading.Thread.join(b)
