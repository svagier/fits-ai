import copy

import numpy as np
from enum import Enum


class FieldType(Enum):
    EMPTY = 0
    TAKEN = 1       # this should always be 1!
    EXTRA_EMPTY = 2
    PLUS_1 = 3
    PLUS_2 = 4
    PLUS_3 = 5
    MINUS_5 = 6
    PAIR_1 = 7
    PAIR_2 = 8
    PAIR_3 = 9
    PAIR_4 = 10
    PAIR_5 = 11


PAIRS_FIELDS = [FieldType.PAIR_1.value, FieldType.PAIR_2.value, FieldType.PAIR_3.value, FieldType.PAIR_4.value,
                FieldType.PAIR_5.value]

# rewritten below so that there is no need to write 'FieldType.' and '.value' every time, so below boards are readable
EMPTY = FieldType.EMPTY.value
EXTRA_EMPTY = FieldType.EXTRA_EMPTY.value
PLUS_1 = FieldType.PLUS_1.value
PLUS_2 = FieldType.PLUS_2.value
PLUS_3 = FieldType.PLUS_3.value
MINUS_5 = FieldType.MINUS_5.value
PAIR_1 = FieldType.PAIR_1.value
PAIR_2 = FieldType.PAIR_2.value
PAIR_3 = FieldType.PAIR_3.value
PAIR_4 = FieldType.PAIR_4.value
PAIR_5 = FieldType.PAIR_5.value


class BoardManager:
    """
    Each Board is 12 Fields high and 6 Fields wide.
    For each Board there are 3 rows of EXTRA_EMPTY. Blocks may be placed there, however neither negative nor positive
    points are given for filling EXTRA_EMPTY Fields. There are 3 rows of EXTRA_EMPTY, because the tallest Blocks
    (Shapes) in the game are 4 Fields high, and there is no point in placing Block solely on EXTRA_EMPTY Fields (there
    will be no points for that).
    """
    def __init__(self):
        self.__extra_empty_rows = np.array(
            [
                [EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY],
                [EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY],
                [EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY]
            ])

        self.__board_1 = np.array(
            [
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
            ])

        self.__board_2 = np.array(
            [
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, PLUS_3, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, PLUS_1, EMPTY],
                [EMPTY, PLUS_2, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, PLUS_3],
                [PLUS_1, PLUS_1, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, PLUS_2, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
            ])

        self.__board_3 = np.array(
            [
                [MINUS_5, EMPTY, EMPTY, EMPTY, EMPTY, MINUS_5],
                [EMPTY, PLUS_1, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, PLUS_1, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, MINUS_5, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, PLUS_3, MINUS_5],
                [EMPTY, PLUS_3, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, MINUS_5, EMPTY, EMPTY, EMPTY, EMPTY],
                [MINUS_5, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [PLUS_2, EMPTY, EMPTY, EMPTY, PLUS_2, MINUS_5],
                [EMPTY, EMPTY, EMPTY, EMPTY, PLUS_2, EMPTY],
                [EMPTY, EMPTY, MINUS_5, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
            ])

        self.__board_4 = np.array(
            [
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, PAIR_5, EMPTY],
                [EMPTY, EMPTY, PAIR_5, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, PAIR_3],
                [PAIR_4, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, PAIR_3, PAIR_4, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, PAIR_1],
                [EMPTY, PAIR_2, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, PAIR_2, EMPTY],
                [PAIR_1, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
            ])

    def get_board(self, board_number: int):
        if board_number == 1:
            return np.concatenate((copy.deepcopy(self.__extra_empty_rows), copy.deepcopy(self.__board_1)))
        elif board_number == 2:
            return np.concatenate((copy.deepcopy(self.__extra_empty_rows), copy.deepcopy(self.__board_2)))
        elif board_number == 3:
            return np.concatenate((copy.deepcopy(self.__extra_empty_rows), copy.deepcopy(self.__board_3)))
        elif board_number == 4:
            return np.concatenate((copy.deepcopy(self.__extra_empty_rows), copy.deepcopy(self.__board_4)))
        else:
            raise Exception("Only 4 boards are available! Valid numbers are 1, 2, 3 and 4.")

    def get_number_of_extra_rows(self):
        return self.__extra_empty_rows.shape[0]
