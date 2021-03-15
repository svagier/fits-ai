import torch
from flask_socketio import SocketIO

from .game import Game, DISCARD_SHAPE_ACTION


class FitsEnv:
    def __init__(self, render: bool = True):
        self.game = Game(random_shapes=False)       # random_shapes = False for DEBUG
        self.game.next_turn()
        self.__render = render
        if render:
            self.__socketio = SocketIO(message_queue='redis://')

    def _board_properties(self):         # get_state_properties()
        return torch.FloatTensor(self.game.board)

    def reset(self):
        if self.__render:
            self.__socketio.emit('board_display', self.game.board.tolist())
        return self._board_properties()

    def get_next_states(self):     # get_next_states()
        # states = {(x_start_column, rotation_number): board_after_this_move}
        return self.game.get_all_possible_states()

    def step(self, action):
        if action != DISCARD_SHAPE_ACTION:
            start_col, rotation_index = action
            self.game.player_place_block(start_col, self.game.current_shape[rotation_index])
        turn_dict = self.game.next_turn(random_shape=False)
        turn_score = turn_dict['score'] - turn_dict['previous_score']
        is_gameover = turn_dict['is_finish']
        if self.__render:
            self.render(turn_dict)
        return turn_score, is_gameover

    def render(self, turn_dict: dict):
        self.__socketio.emit('board_display', self.game.board.tolist())
        self.__socketio.emit('extra_current_stats', self.game.get_extra_current_stats())
        if turn_dict['is_finish']:
            final_score = self.game.calculate_total_score()
            self.__socketio.emit('finished_game', final_score)
        else:
            if 'new_shape' in turn_dict.keys():
                self.__socketio.emit('current_shape', turn_dict['new_shape'])
            if 'remaining_shapes' in turn_dict.keys():
                self.__socketio.emit('remaining_shapes', turn_dict['remaining_shapes'])
            score = self.game.calculate_total_score()
            self.__socketio.emit('display_score', score)

