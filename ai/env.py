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
        # self.action_space = gym.spaces.Discrete(6)  # for humans: Left, Right, Rotate left, Rotate right, Drop, Discard
        self.action_space = gym.spaces.Tuple((
            gym.spaces.Discrete(self.game.board.shape[1]),  # number of columns
            gym.spaces.Discrete(self.game.shapes_manager.get_max_possible_rotations()),  # Number of rotations; currently taking max number of possible rotations for any shape
            # TODO should consider changing size of action_space depending on current Shape: https://stackoverflow.com/questions/45001361/is-there-a-way-to-implement-an-openais-environment-where-the-action-space-chan
        ))
        self.observation_space = gym.spaces.Box(low=FieldType.get_lowest_enum_value(),          # https://github.com/openai/gym/blob/master/gym/spaces/box.py
                                                high=FieldType.get_highest_enum_value(),
                                                shape=self.game.board.shape,
                                                dtype=self.game.board.dtype)

    # def reset(self):
    #     """Starts a new game."""
    #     self.game = self.__get_new_game()
    #     return np.array(self.game.get_all_possible_states())      # TODO

    @staticmethod
    def __get_new_game() -> Game:
        return Game(BOARD_NUMBER)
