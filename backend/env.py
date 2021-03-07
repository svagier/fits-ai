import torch

from .game import Game, DISCARD_SHAPE_ACTION


class FitsEnv:
    def __init__(self):
        self.game = Game(random_shapes=False)       # random_shapes = False for DEBUG
        self.game.next_turn()

    def _board_properties(self):         # get_state_properties()
        return torch.FloatTensor(self.game.board)

    def reset(self):
        return self._board_properties()

    def get_next_states(self):     # get_next_states()
        # states = {(x_start_column, rotation_number): board_after_this_move}
        return self.game.get_all_possible_states()

    def step(self, action, render=True):
        if action != DISCARD_SHAPE_ACTION:
            start_col, rotation_index = action
            self.game.player_place_block(start_col, self.game.current_shape[rotation_index])

        turn_dict = self.game.next_turn(random_shape=False)
        turn_score = turn_dict['score'] - turn_dict['previous_score']
        is_gameover = turn_dict['is_finish']
        return turn_score, is_gameover


