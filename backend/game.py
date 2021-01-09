import random

import numpy as np

from backend.boards import BOARD_1
from backend.shapes import ALL_SHAPES


class Game:
    def __init__(self, board: [np.array] = BOARD_1):
        self.all_shapes = ALL_SHAPES
        self.board = board
        self.__initial_board = board
        self.__board_height = board.shape[0]
        self.__board_width = board.shape[1]
        self.__taken_board = np.zeros((self.__board_height, self.__board_width), dtype=int)
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

    def can_place_block(self, start_row: int, start_col: int, block: np.array) -> bool:
        changed_part_of_board = self.__taken_board[start_row:start_row + block.shape[0], start_col:start_col + block.shape[1]] + block
        print("Changed part of board:", changed_part_of_board)
        if 2 in changed_part_of_board:
            print('Cannot place block here!')
            return False
        else:
            print('Block can be placed here.')
            return True

    def place_block(self, start_row: int, start_col: int, block: np.array):
        self.__taken_board[start_row:start_row + block.shape[0], start_col:start_col + block.shape[1]] += block
        # TODO add for self.board ?

    def run_game(self):
        print('in run_game')
        run = True
        while run:
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
