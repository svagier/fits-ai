import unittest

import numpy as np

from backend.boards import FieldType, BOARD_1, BOARD_2, BOARD_3, BOARD_4, PAIRS_FIELDS


class BoardsContainingAllowedFields(unittest.TestCase):
    """
    Test if all boards (BOARD_1, BOARD_2, BOARD_3, BOARD_4) contain only fields (specified by FieldType enum) which are
    valid for this type of board.
    """
    def test_if_board_1_contains_only_allowed_fields(self):
        allowed_fields_for_board_1 = [FieldType.EMPTY.value, FieldType.EXTRA_EMPTY.value]
        for field in np.nditer(BOARD_1):
            self.assertIn(field, allowed_fields_for_board_1)

    def test_if_board_2_contains_only_allowed_fields(self):
        allowed_fields_for_board_2 = [FieldType.EMPTY.value, FieldType.EXTRA_EMPTY.value, FieldType.PLUS_1.value,
                                      FieldType.PLUS_2.value, FieldType.PLUS_3.value]
        for field in np.nditer(BOARD_2):
            self.assertIn(field, allowed_fields_for_board_2)

    def test_if_board_3_contains_only_allowed_fields(self):
        allowed_fields_for_board_3 = [FieldType.EMPTY.value, FieldType.EXTRA_EMPTY.value, FieldType.PLUS_1.value,
                                      FieldType.PLUS_2.value, FieldType.PLUS_3.value, FieldType.MINUS_5.value]
        for field in np.nditer(BOARD_3):
            self.assertIn(field, allowed_fields_for_board_3)

    def test_if_board_4_contains_only_allowed_fields(self):
        allowed_fields_for_board_4 = [FieldType.EMPTY.value, FieldType.EXTRA_EMPTY.value, FieldType.PAIR_1.value,
                                      FieldType.PAIR_2.value, FieldType.PAIR_3.value, FieldType.PAIR_4.value,
                                      FieldType.PAIR_5.value]
        for field in np.nditer(BOARD_4):
            self.assertIn(field, allowed_fields_for_board_4)


class BoardsMiscellaneousChecks(unittest.TestCase):
    """
    Miscellaneous tests for boards (BOARD_1, BOARD_2, BOARD_3, BOARD_4).
    """
    def test_if_taken_equals_one(self):
        self.assertEqual(FieldType.TAKEN.value, 1)

    def test_if_all_pair_fields_in_PAIRS_FIELDS(self):
        correct_pair_fields = [FieldType.PAIR_1.value, FieldType.PAIR_2.value, FieldType.PAIR_3.value,
                               FieldType.PAIR_4.value, FieldType.PAIR_5.value]
        self.assertEqual(len(correct_pair_fields), len(PAIRS_FIELDS))
        self.assertEqual(set(correct_pair_fields), set(PAIRS_FIELDS))

    def test_if_all_boards_are_the_same_size(self):
        self.assertEqual(BOARD_1.shape, BOARD_2.shape)
        self.assertEqual(BOARD_2.shape, BOARD_3.shape)
        self.assertEqual(BOARD_3.shape, BOARD_4.shape)


if __name__ == '__main__':
    unittest.main()
