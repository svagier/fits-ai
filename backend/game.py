import random

import numpy as np

from backend.boards import FieldType, PAIRS_FIELDS, BoardManager
from backend.shapes import ShapesManager


class Game:
    def __init__(self, board_number: int = 1):
        self.__board_manager = BoardManager()
        self.board_number = board_number
        if board_number in [1, 2, 3, 4]:        # allowed numbers of boards
            self.board = self.__board_manager.get_board(board_number)       # on this board changes will be put
            self.__initial_board = self.__board_manager.get_board(board_number)     # this board will remain unchanged
        else:       # BOARD_1 is default if board_number is wrong
            print('Passed in wrong number of board ({}). Using default board - board number 1.'.format(board_number))
            self.board = self.__board_manager.get_board(1)
            self.__initial_board = self.__board_manager.get_board(1)
        self.number_of_extra_rows_on_board = self.__board_manager.get_number_of_extra_rows()
        self.board_height = self.board.shape[0]     # board height including extra rows (number_of_extra_rows_on_board)
        self.board_width = self.board.shape[1]
        self.__taken_board = np.zeros((self.board_height, self.board_width), dtype=int)
        self.__column_peaks_row_indexes = np.array([self.board_height - 1 for i in range(0, self.board_width)], dtype=int)
        self.__shapes_manager = ShapesManager()
        self.names_of_initial_shapes = self.__shapes_manager.get_names_of_initial_shapes()
        self.remaining_shapes_dict = self.__shapes_manager.get_all_shapes_dict()
        self.current_shape = None
        self.turn_number = 0         # 0 means that the game has not started yet. Number of the first turn when move is possible is 1. It will be incremented to 1 in next_turn()
        self.is_finish = False

    def get_random_shape(self):
        number_of_remaining_shapes = len(self.remaining_shapes_dict)
        if number_of_remaining_shapes == 0:
            self.is_finish = True
            return
        if self.turn_number == 1:       # first turn number is 1
            random_shape_name = random.choice(self.names_of_initial_shapes)
        else:
            random_index = random.randrange(0, number_of_remaining_shapes)
            random_shape_name = list(self.remaining_shapes_dict.keys())[random_index]
        self.current_shape = self.remaining_shapes_dict.pop(random_shape_name)
        return self.current_shape

    def get_board(self) -> np.array:
        return self.board

    def get_taken_board(self) -> np.array:
        return self.__taken_board

    """This method should be used only for tests! (game_score_tests.py)"""
    def set_taken_board(self, new_taken_board: np.array):
        self.__taken_board = new_taken_board

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
        if self.is_finish:
            return False
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
                    if field_value_on_board == FieldType.TAKEN.value:
                        raise Exception('If this exception is raised, it means that there is a bug and this block'
                                        'should not be placed here. It should have been never allowed to this function '
                                        '(update_main_board).')     # for DEBUG, need to comment out later TODO
                    self.board[row_num, col_num] = FieldType.TAKEN.value
                    # elif: add handling for PAIRS handling TODO

    def place_block(self, start_row: int, start_col: int, block: np.array):
        block_height, block_width = block.shape
        end_row = start_row + block_height            # this row will not be included (exclusive indexing)
        end_col = start_col + block_width             # this column will not be included (exclusive indexing)
        self.update_taken_board(start_row, end_row, start_col, end_col, block)
        self.update_main_board(start_row, end_row, start_col, end_col, block)
        self.update_column_peaks_row_indexes(start_col, end_col)

    """TODO add comment that id returns only serializable data, so np.arrays are converted to lists"""
    def next_turn(self) -> dict:
        new_shape_list = None
        remaining_shapes_list = None
        if not self.is_finish:
            self.turn_number += 1
            new_shape = self.get_random_shape()
            if new_shape:
                new_shape_list = [nparray.tolist() for nparray in new_shape]
            if self.remaining_shapes_dict:
                remaining_shapes_list = [nparray[0].tolist() for nparray in list(self.remaining_shapes_dict.values())]
            else:
                remaining_shapes_list = None

        data = {
            "turn_number": self.turn_number,
            "is_finish": self.is_finish,
            "score": 0,     #TODO
            "new_shape":  new_shape_list,
            "remaining_shapes": remaining_shapes_list
        }
        return data

    def calculate_total_score(self) -> int:
        if self.board_number == 1:
            return self.calculate_total_score_board_1()
        elif self.board_number == 2:
            return self.calculate_total_score_board_2()
        elif self.board_number == 3:
            return self.calculate_total_score_board_3()
        elif self.board_number == 4:
            return self.calculate_total_score_board_4()
        else:
            return Exception('Board numbers should be in range <1; 4>!')

    def calculate_total_score_board_1(self) -> int:
        total_score = 0
        for row_index, row_value in enumerate(self.__taken_board):
            if row_index < self.number_of_extra_rows_on_board:
                continue                    # ignore blocks placed in extra rows (rows with EXTRA_EMPTY fields)
            row_completed = True
            for col_index, col_value in enumerate(row_value):
                initial_field_value = self.__initial_board[row_index, col_index]
                if col_value == 0:
                    row_completed = False
                    if initial_field_value == FieldType.EMPTY.value:
                        total_score -= 1
            if row_completed:
                total_score += 1
        return total_score

    def calculate_total_score_board_2(self) -> int:
        total_score = 0
        for row_index, row_value in enumerate(self.__taken_board):
            if row_index < self.number_of_extra_rows_on_board:
                continue                    # ignore blocks placed in extra rows (rows with EXTRA_EMPTY fields)
            for col_index, col_value in enumerate(row_value):
                initial_field_value = self.__initial_board[row_index, col_index]
                if col_value == 0:
                    if initial_field_value == FieldType.EMPTY.value:
                        total_score -= 1
                    elif initial_field_value == FieldType.PLUS_1.value:
                        total_score += 1
                    elif initial_field_value == FieldType.PLUS_2.value:
                        total_score += 2
                    elif initial_field_value == FieldType.PLUS_3.value:
                        total_score += 3
        return total_score

    def calculate_total_score_board_3(self) -> int:
        total_score = 0
        for row_index, row_value in enumerate(self.__taken_board):
            if row_index < self.number_of_extra_rows_on_board:
                continue                    # ignore blocks placed in extra rows (rows with EXTRA_EMPTY fields)
            for col_index, col_value in enumerate(row_value):
                initial_field_value = self.__initial_board[row_index, col_index]
                if col_value == 0:
                    if initial_field_value == FieldType.EMPTY.value:
                        total_score -= 1
                    elif initial_field_value == FieldType.MINUS_5.value:
                        total_score -= 5
                    elif initial_field_value == FieldType.PLUS_1.value:
                        total_score += 1
                    elif initial_field_value == FieldType.PLUS_2.value:
                        total_score += 2
                    elif initial_field_value == FieldType.PLUS_3.value:
                        total_score += 3
        return total_score

    def calculate_total_score_board_4(self) -> int:
        total_score = 0
        pair_fields_uncovered = {}
        for pair_field_type in PAIRS_FIELDS:
            pair_fields_uncovered[pair_field_type] = 0
        for row_index, row_value in enumerate(self.__taken_board):
            if row_index < self.number_of_extra_rows_on_board:
                continue                    # ignore blocks placed in extra rows (rows with EXTRA_EMPTY fields)
            for col_index, col_value in enumerate(row_value):
                initial_field_value = self.__initial_board[row_index, col_index]
                if col_value == 0:
                    if initial_field_value == FieldType.EMPTY.value:
                        total_score -= 1
                    elif initial_field_value in PAIRS_FIELDS:
                        pair_fields_uncovered[initial_field_value] += 1
        for number_of_uncovered_pair_fields in pair_fields_uncovered.values():
            if number_of_uncovered_pair_fields == 2:
                total_score += 3
            elif number_of_uncovered_pair_fields == 1:
                total_score -= 3
        return total_score

    def get_extra_current_stats(self) -> dict:
        current_shape_fields_taken = int(np.sum(self.current_shape[0]))
        remaining_shapes_fields_taken = 0
        for shape in self.remaining_shapes_dict.values():
            remaining_shapes_fields_taken += int(np.sum(shape[0]))
        all_empty_remaining_fields = 0
        empty_unreachable_fields = 0
        for row_index, row_value in enumerate(self.__taken_board):
            for col_index, col_value in enumerate(row_value):
                if self.__initial_board[row_index, col_index] != FieldType.EXTRA_EMPTY.value:
                    if col_value == 0:
                        all_empty_remaining_fields += 1
                        if row_index > 0:
                            if self.__taken_board[row_index - 1, col_index] == 1:
                                empty_unreachable_fields += 1

        return {
            "taken_fields_in_current_shape": current_shape_fields_taken,
            "taken_fields_in_remaining_shapes_without_current": remaining_shapes_fields_taken,
            "all_empty_reachable_fields": all_empty_remaining_fields - empty_unreachable_fields,
            "empty_unreachable_fields": empty_unreachable_fields
        }
