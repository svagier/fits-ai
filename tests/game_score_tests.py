import unittest

import numpy as np

from backend.game import Game


class ScoreCountingForInitialBoardsTest(unittest.TestCase):
    """Test if Game's function calculate_total_score() gives correct score for original, initial boards."""
    def test_initial_score_for_board_1(self):
        game = Game(1)
        initial_total_score = game.calculate_total_score()
        correct_score = -72                         # -72 points: 6 * 12 unfilled fields, -1 for each field
        self.assertEqual(initial_total_score, correct_score)

    def test_initial_score_for_board_2(self):
        game = Game(2)
        initial_total_score = game.calculate_total_score()
        correct_score = -65 + 3*1 + 2*2 + 2*3       # -1 for each empty field (-65)  + extra points for plus fields
        self.assertEqual(initial_total_score, correct_score)

    def test_initial_score_for_board_3(self):
        game = Game(3)
        initial_total_score = game.calculate_total_score()
        correct_score = -57 - 8*5 + 2*1 + 3*2 + 2*3                 # -1 for each empty field (-57) - points for minus
        self.assertEqual(initial_total_score, correct_score)        # fields + extra points for plus fields

    def test_initial_score_for_board_4(self):
        game = Game(4)
        initial_total_score = game.calculate_total_score()
        correct_score = -62 + 5*3       # -1 for each empty field (-62)  + extra 3 points for each uncovered pair
        self.assertEqual(initial_total_score, correct_score)
        

class ScoreCountingForCustomBoardsTest(unittest.TestCase):
    """Test if Game's function calculate_total_score() gives correct score for custom, partially filled boards."""
    def test_total_score_for_custom_filled_board_1(self):
        game = Game(1)
        custom_taken_board = np.array(
            [
                [1, 1, 1, 1, 1, 1],         # this row should not affect the score - it is row of EXTRA_EMPTY fields
                [1, 0, 1, 0, 0, 0],         # this row should not affect the score - it is row of EXTRA_EMPTY fields
                [1, 0, 0, 0, 1, 0],         # this row should not affect the score - it is row of EXTRA_EMPTY fields
                [1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 1, 0],
                [1, 0, 0, 1, 0, 0],
                [1, 0, 1, 0, 0, 0],
                [1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1]          # + 1 for full filled row
            ])
        correct_score = -49
        game.set_taken_board(custom_taken_board)
        game_score = game.calculate_total_score()
        self.assertEqual(game_score, correct_score)


if __name__ == '__main__':
    unittest.main()
