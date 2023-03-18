import tkinter as tk
import tkinter.ttk as ttk

# import tk


class Window:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.size = 7
        self.labels = []
        self.draw()

    def handleClick(self, event: tk.Event) -> None:
        label = event.widget
        label.config(bg="yellow")
        print(label.cget("text"), label._name)

    def markPoint(self, position: int) -> None:
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
                label = tk.Label(master=frame, text=f"{i} {j}", name=f"{i},{j}")
                

                label.bind("<Button-1>", self.handleClick)
                temp.append(label)

                # expand=True makes the text centered inside the label
                # fill makes it fill the frame excluding the padding
                label.pack(padx=5, pady=5, expand=True, fill=tk.BOTH)
            self.labels.append(temp)

        # fill=tk.BOTH makes the grid_frame expand
        # in X and Y axis when window is resized
        grid_frame.pack(fill=tk.BOTH, expand=True)
        self.window.mainloop()


a = Window()
