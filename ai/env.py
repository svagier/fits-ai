import gym

from backend.boards import FieldType
from backend.game import Game

BOARD_NUMBER = 1        # TODO shouldn't this be passed as parameter?


class FitsEnv(gym.Env):
    def __init__(self):
        super(FitsEnv, self).__init__()
        self.game = self.__get_new_game()
        # # Set this in SOME subclasses
        # metadata = {'render.modes': []}
        # reward_range = (-float('inf'), float('inf'))
        # spec = None

        # Set these in ALL subclasses
        # Left, Right, Rotate left, Rotate right, Drop, Discard
        self.action_space = gym.spaces.Discrete(6)
        self.observation_space = gym.spaces.Box(low=FieldType.get_lowest_enum_value(),          # https://github.com/openai/gym/blob/master/gym/spaces/box.py
                                                high=FieldType.get_highest_enum_value(),
                                                shape=self.game.board.shape,
                                                dtype=self.game.board.dtype)

    # def reset(self):
    #     """Starts a new game."""
    #     self.game = self.__get_new_game()
    #     return np.array(self.game.board.get_possible_states())      # TODO

    @staticmethod
    def __get_new_game() -> Game:
        return Game(BOARD_NUMBER)
