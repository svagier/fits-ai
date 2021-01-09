import random

import numpy as np

from backend.boards import BOARD_1
from backend.shapes import ALL_SHAPES


class Game:
    def __init__(self, board: [np.array] = BOARD_1):
        self.all_shapes = ALL_SHAPES
        self.board = board
        self.__initial_board = board
        self.board_height = board.shape[0]
        self.board_width = board.shape[1]
        self.__taken_board = np.zeros((self.board_height, self.board_width), dtype=int)
        self.__column_peaks_row_indexes = np.array([self.board_height - 1 for i in range(0, self.board_width)], dtype=int)
        self.current_shape = None

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

    def get_taken_board(self) -> np.array:
        return self.__taken_board

    """end_col is not inclusive, just like with slicing lists"""
    def update_column_peaks_row_indexes(self, start_col: int, end_col: int):
        for col_index, column in enumerate(self.__taken_board.T):
            if start_col <= col_index < end_col:
                for row_index, field_value in enumerate(column):
                    if field_value > 0:       # taken space
                        self.__column_peaks_row_indexes[col_index] = row_index - 1
                        break

    def is_column_index_correct(self, col_index: int, block: np.array) -> bool:
        block_width = len(block[0])
        if col_index + block_width <= self.board_width:
            return True
        else:
            print("{} is incorrect column index (block is {} fields wide and the board's last index is {}."
                  .format(col_index, block_width, self.board_width - 1))
            return False

    """Row numbers start from top (row number 0 at top of the displayed board)."""
    def find_start_row(self, start_col: int, block: np.array) -> int:
        block_width = len(block[0])
        peaks_of_columns_below_block = self.__column_peaks_row_indexes[start_col:start_col+block_width]
        initial_start_row_index = min(peaks_of_columns_below_block)
        start_row_index = initial_start_row_index
        while start_row_index >= 0:
            if self.can_place_block(start_row_index, start_col, block):
                return start_row_index
            else:
                start_row_index -= 1
        return None

    def can_place_block(self, start_row: int, start_col: int, block: np.array) -> bool:
        end_row = start_row + block.shape[0]
        end_col = start_col + block.shape[1]
        if end_row > self.board_height or end_col > self.board_width:
            print('Cannot place block outside the Board!')
            return False
        part_of_board_to_be_changed = self.__taken_board[start_row:end_row, start_col:end_col]
        changed_part_of_board = part_of_board_to_be_changed + block
        if 2 in changed_part_of_board:      # the block to be placed overlaps some taken field
            print('Cannot place block here!')
            return False
        else:
            print('Block can be placed here.')
            return True

    def player_place_block(self, start_col: int, block: np.array) -> bool:
        if self.is_column_index_correct(start_col, block):
            start_row = self.find_start_row(start_col, block)
            if not start_row:
                return False
            self.place_block(start_row, start_col, block)
            return True
        else:
            return False

    def place_block(self, start_row: int, start_col: int, block: np.array):
        end_row = start_row + block.shape[0]            # this row will not be included (exclusive indexing)
        end_col = start_col + block.shape[1]            # this column will not be included (exclusive indexing)
        self.__taken_board[start_row:end_row, start_col:end_col] += block
        self.board[start_row:end_row, start_col:end_col] += block
        self.update_column_peaks_row_indexes(start_col, end_col)

    def run_game(self):
        print('in run_game')
        run = True
        while run:
            self.current_shape = self.get_random_shape()
            yield {'current_shape': self.current_shape}
            run = False


#
# def main():
#     print_shapes()
#
#
# if __name__ == "__main__":
#     main()
