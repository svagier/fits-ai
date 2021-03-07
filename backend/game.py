import copy
import random

import numpy as np
import torch

from backend.boards import FieldType, PAIRS_FIELDS, BoardManager
from backend.shapes import ShapesManager

DISCARD_SHAPE_ACTION = ('discard', 'discard')     # TODO put it in better place?


class Game:
    def __init__(self, board_number: int = 1, random_shapes: bool = True):
        self.__board_manager = BoardManager()
        self.board_number = board_number
        if board_number in [1, 2, 3, 4]:        # allowed numbers of boards
            self.board = self.__board_manager.get_board(board_number)       # on this board changes will be put
            self.__initial_board = self.__board_manager.get_board(board_number)     # this board will remain unchanged
        else:       # BOARD_1 is default if board_number is wrong
            print('Passed in wrong number of board ({}). Using default board - board number 1.'.format(board_number))
            self.board = self.__board_manager.get_board(1)
            self.__initial_board = self.__board_manager.get_board(1)
        self.random_shapes = random_shapes
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
        self.__previous_score = self.calculate_total_score()

    def get_next_shape(self) -> np.array:
        if self.random_shapes:
            return self.__get_random_shape()
        else:
            return self.__get_next_shape_in_order()

    def __get_random_shape(self):
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

    def __get_next_shape_in_order(self):
        number_of_remaining_shapes = len(self.remaining_shapes_dict)
        if number_of_remaining_shapes == 0:
            self.is_finish = True
            return
        if self.turn_number == 1:       # first turn number is 1
            shape_name = self.names_of_initial_shapes[0]
        else:
            shape_name = list(self.remaining_shapes_dict.keys())[0]
        self.current_shape = self.remaining_shapes_dict.pop(shape_name)
        return self.current_shape

    def get_board(self) -> np.array:
        return self.board

    def get_taken_board(self) -> np.array:
        return self.__taken_board

    def set_taken_board(self, new_taken_board: np.array):
        """This method should be used only for tests! (game_score_tests.py)"""
        self.__taken_board = new_taken_board

    def update_column_peaks_row_indexes(self, start_col: int, end_col: int):
        """end_col is not inclusive, just like with slicing lists"""
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

    def find_start_row(self, start_col: int, block: np.array) -> int:
        """Row numbers start from top (row number 0 at top of the displayed board)."""
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

    def place_block(self, start_row: int, start_col: int, block: np.array):
        block_height, block_width = block.shape
        end_row = start_row + block_height            # this row will not be included (exclusive indexing)
        end_col = start_col + block_width             # this column will not be included (exclusive indexing)
        self.update_taken_board(start_row, end_row, start_col, end_col, block)
        self.update_main_board(start_row, end_row, start_col, end_col, block)
        self.update_column_peaks_row_indexes(start_col, end_col)

    def place_rotated_shape(self, start_row: int, start_col: int, rotation_number: int):
        if rotation_number >= len(self.current_shape) or rotation_number < 0:
            raise IndexError('Rotation number {} is an index out of bounds for current shape, which has 0 as minimum '
                             'index and {} as maximum index.'.format(rotation_number, len(self.current_shape)))
        self.place_block(start_row, start_col, self.current_shape[rotation_number])

    def next_turn(self, random_shape=True) -> dict:
        """
        The data dict returned by this function will be then sent as json to frontend, so np.arrays (new_shape_list
        and remaining_shapes_list) have to be converted to regular Python lists, since np.arrays are not serializable.
        """
        new_shape_list = None
        remaining_shapes_list = None
        if not self.is_finish:
            self.turn_number += 1
            print('Turn number: ', self.turn_number)
            new_shape = self.get_next_shape()
            if new_shape:
                new_shape_list = [nparray.tolist() for nparray in new_shape]
            if self.remaining_shapes_dict:
                remaining_shapes_list = [nparray[0].tolist() for nparray in list(self.remaining_shapes_dict.values())]
            else:
                remaining_shapes_list = None

        total_score = self.calculate_total_score()
        data = {
            "turn_number": self.turn_number,
            "is_finish": self.is_finish,
            "previous_score": self.__previous_score,
            "score": total_score,
            "new_shape":  new_shape_list,
            "remaining_shapes": remaining_shapes_list
        }
        self.__previous_score = total_score
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

    def __get_board_after_potential_move(self, start_row: int, start_col: int, block: np.array) -> np.array:
        block_height, block_width = block.shape
        end_row = start_row + block_height  # this row will not be included (exclusive indexing)
        end_col = start_col + block_width  # this column will not be included (exclusive indexing)
        new_board = copy.deepcopy(self.board)
        for row_num in range(start_row, end_row):
            for col_num in range(start_col, end_col):
                incoming_block_exists_on_this_field = block[row_num - start_row, col_num - start_col] == 1
                if incoming_block_exists_on_this_field:
                    field_value_on_board = new_board[row_num, col_num]
                    if field_value_on_board == FieldType.TAKEN.value:
                        raise Exception('If this exception is raised, it means that there is a bug and this block'
                                        'should not be placed here. It should have been never allowed to this function '
                                        '(update_main_board).')  # for DEBUG, need to comment out later TODO
                    new_board[row_num, col_num] = FieldType.TAKEN.value
        return new_board

    # def get_all_possible_states(self) -> [((int, int, int), np.array)]:
    #     """
    #     Tries out every possible move for every rotation of the current Shape and returns all possible states of the
    #     board (all possible boards).
    #     Currently state is the board - 2D array. In the future it may be changed, for example [peaks, remaining shapes,
    #     covered pairs] etc.
    #
    #     Returns:
    #     states - list of tuples (action, state), where:
    #         action (tuple(int, int, int)) = (start_row_index, start_col_index, index_of_rotation)
    #         state (np.array) = board after given move
    #     """
    #     states = []
    #     # add state for discarding block # TODO research
    #     states.append((DISCARD_SHAPE_ACTION, copy.deepcopy(self.board)))
    #     for index_of_rotation, rotated_shape in enumerate(self.current_shape):
    #         for start_col_index in range(0, self.board_width - rotated_shape.shape[1]):
    #             start_row_index = self.find_start_row(start_col_index, rotated_shape)
    #             if start_row_index:     # it may be possible that given block cannot be put in this column
    #                 action = (start_row_index, start_col_index, index_of_rotation)
    #                 state = self.__get_board_after_potential_move(start_row_index, start_col_index, rotated_shape)
    #                 states.append((action, state))
    #     if not states:
    #         self.print_board_to_terminal()
    #     return states

    def get_all_possible_states(self) -> [((int, int, int), np.array)]:
        """ returns:  states = {(x_start_column, rotation_number): board_after_this_move} """
        states = {}
        # state for discarding block:
        states[DISCARD_SHAPE_ACTION] = torch.FloatTensor(copy.deepcopy(self.board))     # should it be deepcopy?
        # states.append((DISCARD_SHAPE_ACTION, copy.deepcopy(self.board)))
        for index_of_rotation, rotated_shape in enumerate(self.current_shape):
            for start_col_index in range(0, self.board_width - rotated_shape.shape[1]):
                start_row_index = self.find_start_row(start_col_index, rotated_shape)
                if start_row_index:     # it may be possible that given block cannot be put in this column
                    action = (start_row_index, start_col_index, index_of_rotation)
                    # state = self.__get_board_after_potential_move(start_row_index, start_col_index, rotated_shape)
                    board_after_move = self.__get_board_after_potential_move(start_row_index, start_col_index, rotated_shape)
                    tensor_board_after_move = torch.FloatTensor(board_after_move)
                    states[(start_col_index, index_of_rotation)] = tensor_board_after_move
        self.print_board_to_terminal()
        print('Number of states: ', len(states))
        return states

    def print_board_to_terminal(self):
        for row in self.board:
            print()
            for elem in row:
                print(elem, end='')
