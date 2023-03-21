from __future__ import annotations
import random
import client
import graphics
import card
from _thread import *


class Opponent:
    def __init__(self, view_window: bool = True) -> None:
        self.view_window = view_window
        self.client = client.BingoClient()
        self.bingo_card = card.Bingo(self.client.game_size)
        self.game_size = self.client.game_size

        if self.view_window:
            self.window = graphics.Window(bingo=self.bingo_card, client=self.client, name="opp")
            self.client.setWindow(window=self.window)
            

    def get_max_point(self) -> list:
        for i in range(self.game_size - 1, 0, -1):
            max_count = self.bingo_card.marked_ele.count(i)
            if max_count > 0:
                data = []
                for j in range(max_count):
                    if self.bingo_card.marked_ele[j] == i:
                        data.append((i, j))
                return data

        return [(0, 0)]

    def get_max_value_in_row_or_column(self, position: int) -> tuple:
        max_unmarked = 0
        max_unmarked_pos = -1

        if position < self.game_size:
            for i in range(self.game_size):
                if self.bingo_card.bingo_matrix[position][i][1] == "False":
                    count = (
                        self.game_size - self.bingo_card.marked_ele[i + self.game_size]
                    )
                    if count > max_unmarked:
                        max_unmarked = count
                        max_unmarked_pos = i + self.game_size
            return position, max_unmarked_pos

        if position < self.game_size * 2:
            for i in range(self.game_size):
                if self.bingo_card.bingo_matrix[i][position][1] == "False":
                    count = self.game_size - self.bingo_card.marked_ele[i]
                    if count > max_unmarked:
                        max_unmarked = count
                        max_unmarked_pos = i
            return position, max_unmarked_pos

        if position == 2 * self.game_size:
            for i in range(self.game_size):
                if self.bingo_card.bingo_matrix[i][i][1] == False:
                    count = self.game_size - self.bingo_card.marked_ele[i]
                    if count > max_unmarked:
                        max_unmarked = count
                        max_unmarked_pos = i

                    count = (
                        self.game_size - self.bingo_card.marked_ele[i + self.game_size]
                    )
                    if count > max_unmarked:
                        max_unmarked = count
                        max_unmarked_pos = i + self.game_size
            return position, max_unmarked_pos

        if position == 2 * self.game_size + 1:
            for i in range(self.game_size):
                if self.bingo_card.bingo_matrix[i][self.game_size - 1 - i][1] == False:
                    count = self.game_size - self.bingo_card.marked_ele[i]
                    if count > max_unmarked:
                        max_unmarked = count
                        max_unmarked_pos = i

                    count = (
                        self.game_size - self.bingo_card.marked_ele[i + self.game_size]
                    )
                    if count > max_unmarked:
                        max_unmarked = count
                        max_unmarked_pos = i + self.game_size
            return position, max_unmarked_pos

    def find_optimal_location(self):
        max_value_data = self.get_max_point()
        indices = []
        if max_value_data[0] != (0, 0):
            for val, pos in max_value_data:
                position, max_unmarked_pos = self.get_max_value_in_row_or_column(pos)
                indices.append((position, max_unmarked_pos))

        print(indices)
        return random.choice(indices)
    
    
    def play(self):
        i, j = self.find_optimal_location()
        self.window.markPoint(i, j)
        self.client.client_send(self.bingo_card.bingo_matrix[i][j][0])




# opponent = Opponent()

# def proc():
#     opponent.client.start_reading()
#     pass


# start_new_thread(proc, ())
# opponent.window.start_loop()

#   1. Algo
#   2. Find the row/cols with max cells marked
#   3. For each row/col :
#       4. Find the unmarked cells that has the most cells marked
#       5. Goto step 2
