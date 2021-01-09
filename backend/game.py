import random

import numpy as np

from backend.boards import BOARD_1
from backend.shapes import ALL_SHAPES


class Game:
    def __init__(self, board: [np.array] = BOARD_1):
        self.all_shapes = ALL_SHAPES
        self.board = board
        self.__board_width = board.shape[1]
        self.__column_peaks = np.zeros((self.__board_width,), dtype=int)

    def print_shapes(self):
        for list_of_rotations in self.all_shapes:
            print('\n\n Shape:', end='')
            for rotated_shape in list_of_rotations:
                print()
                for row_list in rotated_shape:
                    print()
                    for elem in row_list:
                        if elem:
                            print('*', end='')
                        else:
                            print(' ', end='')

    def get_random_shape(self):
        return random.choice(self.all_shapes)

    def get_board(self) -> np.array:
        return self.board

    def run_game(self):
        print('in run_game')
        run = True
        while run:         # TODO add key handling
            current_block = self.get_random_shape()
            yield {'current_block': current_block}
            run = False


#
# def main():
#     print_shapes()
#
#
# if __name__ == "__main__":
#     main()
