import random
import threading
import time
import tkinter as tk
# import tkinter.ttk as ttk
from card import Bingo


class Window:
    
    def __init__(self, bingo: Bingo) -> None:
        self.root = tk.Tk(className="Bingo")
        self.bingo = bingo
        self.size = bingo.row
        self.points = 0
        self.bingo_matrix = bingo.bingo_matrix
        self.labels = []
        # self.window.wm_/
        self.draw()

    def handleClick(self, event: tk.Event) -> None:
        label = event.widget
        indices = list(map(lambda x: int(x), label._name.split(" ")))

        if not self.bingo_matrix[indices[0]][indices[1]][1]:
            # print(label.cget("text"), label._name)
            label.config(bg="yellow")
            self.bingo_matrix[indices[0]][indices[1]][1] = True
            self.bingo.marked_entry(indices[0], indices[1])

            for i in range(2 * self.size + 2):
                if self.bingo.marked_ele[i] == self.size:
                    self.markLine(i)

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

    def draw(self) -> None:
        grid_frame = tk.Frame()

        for i in range(self.size):
            # Make the grid responsive
            grid_frame.rowconfigure(i, weight=1, minsize=75)
            grid_frame.columnconfigure(i, weight=1, minsize=75)
            temp = []
            for j in range(self.size):
                frame = tk.Frame(master=grid_frame, relief=tk.RAISED, borderwidth=1)

                # sticky='nesw' since individual frames have
                # to expand to all directions when resized
                frame.grid(row=i, column=j, padx=5, pady=5, sticky="nesw")
                label = tk.Label(
                    master=frame, text=f"{self.bingo_matrix[i][j][0]}", name=f"{i} {j}"
                )

                label.bind("<Button-1>", self.handleClick)
                temp.append(label)

                # expand=True makes the text centered inside the label
                # fill makes it fill the frame excluding the padding
                label.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)
            self.labels.append(temp)

        # fill=tk.BOTH makes the grid_frame expand
        # in X and Y axis when window is resized
        grid_frame.pack(fill=tk.BOTH, expand=True)
        # self.markLine(14)
        # self.root.mainloop()



class App(threading.Thread):
    def __init__(self, a):
        self.a = a
        threading.Thread.__init__(self)
        pass
    
    def get(self):
        return self.w
    
    def run(self):
        while True:
            time.sleep(1)
            x, y = random.randint(0, 4), random.randint(0, 4)
            print(x, y)
            a.markPoint(x, y)
            # a.markLine(x  + y)


a = Window(Bingo(5))
b = App(a)
b.start()
a.root.mainloop()
# threading.Thread.join(b)
