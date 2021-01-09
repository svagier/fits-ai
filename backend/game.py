import random

import numpy as np

from backend.boards import BOARD_1, FieldType
from backend.shapes import ALL_SHAPES


class Game:
    def __init__(self, board: [np.array] = BOARD_1):
        self.remaining_shapes = ALL_SHAPES
        self.board = board
        self.__initial_board = board
        self.board_height = board.shape[0]
        self.board_width = board.shape[1]
        self.__taken_board = np.zeros((self.board_height, self.board_width), dtype=int)
        self.__column_peaks_row_indexes = np.array([self.board_height - 1 for i in range(0, self.board_width)], dtype=int)
        self.current_shape = None
        self.turn_number = 0
        self.is_finish = False

    def get_random_shape(self):
        number_of_remaining_shapes = len(self.remaining_shapes)
        if number_of_remaining_shapes == 0:
            self.is_finish = True
            return
        random_index = random.randrange(0, number_of_remaining_shapes)
        self.current_shape = self.remaining_shapes.pop(random_index)
        return self.current_shape

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
        block_height, block_width = block.shape
        peaks_of_columns_below_block = self.__column_peaks_row_indexes[start_col:start_col+block_width]
        highest_column_index = min(peaks_of_columns_below_block)
        shortest_column_index = max(peaks_of_columns_below_block)
        initial_start_row_index = highest_column_index - block_height + 1
        if initial_start_row_index not in range(0, self.board_height):
            initial_start_row_index = 0
        last_valid_row_index = None
        if self.can_place_block(initial_start_row_index, start_col, block):
            last_valid_row_index = initial_start_row_index
        else:
            return None
        start_row_index = initial_start_row_index
        while start_row_index <= shortest_column_index:
            if not self.can_place_block(start_row_index, start_col, block):
                break
            else:
                last_valid_row_index = start_row_index
                start_row_index += 1
        if last_valid_row_index is None:
            raise Exception
        else:
            return last_valid_row_index

    def can_place_block(self, start_row: int, start_col: int, block: np.array) -> bool:
        block_height, block_width = block.shape
        end_row = start_row + block_height
        end_col = start_col + block_width
        if end_row > self.board_height or end_col > self.board_width:   # block would be outside the Board
            return False
        part_of_board_to_be_changed = self.__taken_board[start_row:end_row, start_col:end_col]
        changed_part_of_board = part_of_board_to_be_changed + block
        if 2 in changed_part_of_board:      # the block to be placed overlaps some taken field
            return False
        else:
            return True

    def player_place_block(self, start_col: int, block: np.array) -> bool:
        if self.is_column_index_correct(start_col, block):
            start_row = self.find_start_row(start_col, block)
            if start_row is None:
                return False
            self.place_block(start_row, start_col, block)
            return True
        else:
            return False

    def update_taken_board(self, start_row: int, end_row: int, start_col: int, end_col: int, block: np.array):
        self.__taken_board[start_row:end_row, start_col:end_col] += block

    def update_main_board(self, start_row: int, end_row: int, start_col: int, end_col: int, block: np.array):
        for row_num in range(start_row, end_row):
            for col_num in range(start_col, end_col):
                incoming_block_exists_on_this_field = block[row_num - start_row, col_num - start_col] == 1
                if incoming_block_exists_on_this_field:
                    field_value_on_board = self.board[row_num, col_num]
                    if field_value_on_board == FieldType.EMPTY.value or field_value_on_board == FieldType.EXTRA_EMPTY.value:
                        self.board[row_num, col_num] = FieldType.TAKEN.value
                    # elif: add handling for PAIRS handling TODO
                    elif field_value_on_board == FieldType.TAKEN.value:
                        raise Exception('If this exception is raised, it means that there is a bug and this block'
                                        'should not be placed here. It should have been never allowed to this function '
                                        '(update_main_board).')     # for DEBUG, need to comment out later TODO

    def place_block(self, start_row: int, start_col: int, block: np.array):
        block_height, block_width = block.shape
        end_row = start_row + block_height            # this row will not be included (exclusive indexing)
        end_col = start_col + block_width             # this column will not be included (exclusive indexing)
        self.update_taken_board(start_row, end_row, start_col, end_col, block)
        self.update_main_board(start_row, end_row, start_col, end_col, block)
        self.update_column_peaks_row_indexes(start_col, end_col)

    def next_turn(self) -> dict:
        new_shape = self.get_random_shape()
        if not self.is_finish:
            self.turn_number += 1
        data = {
            "turn_number": self.turn_number,
            "is_finish": self.is_finish,
            "score": 0,     #TODO
            "new_shape": new_shape
        }
        return data
