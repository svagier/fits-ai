import unittest

import numpy as np

from backend.boards import FieldType, BOARD_1, BOARD_2, BOARD_3, BOARD_4


class BoardsContainingAllowedFields(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
