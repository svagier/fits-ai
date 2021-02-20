import copy

import numpy as np


class ShapesManager:
    """
    Each shape contains lists describing its rotations. Each next rotation of shape is rotated by 90 degrees clockwise
    relative to the previous rotation. After all rotations for one 'side' of the Shape have been written in lists, next
    lists describe the shape when it is 'turned over' (mirrored). Each mirrored rotation is also rotated by 90 degrees
    clockwise. In other words, half of the subarrays will be for normal rotations of shape, half of the subarrays will
    be for mirrored rotations.
    It is possible for a shape not to have a mirrored versions (if it is rotationally symmetric or if mirrored rotations
    are the same as original rotations).
    """
    def __init__(self):
        self.__LONG_L = \
            [
                np.array([
                        [1, 0],
                        [1, 0],
                        [1, 0],
                        [1, 1]
                ]),
                np.array([
                        [1, 1, 1, 1],
                        [1, 0, 0, 0]
                ]),
                np.array([
                        [1, 1],
                        [0, 1],
                        [0, 1],
                        [0, 1]
                ]),
                np.array([
                        [0, 0, 0, 1],
                        [1, 1, 1, 1]
                ]),
                # mirrored below
                np.array([
                        [0, 1],
                        [0, 1],
                        [0, 1],
                        [1, 1]
                ]),
                np.array([
                        [1, 0, 0, 0],
                        [1, 1, 1, 1]
                ]),
                np.array([
                        [1, 1],
                        [1, 0],
                        [1, 0],
                        [1, 0]
                ]),
                np.array([
                        [1, 1, 1, 1],
                        [0, 0, 0, 1]
                ])
            ]

        self.__P_SHAPE = \
            [
                np.array([
                        [1, 1],
                        [1, 1],
                        [1, 0]
                ]),
                np.array([
                        [1, 1, 1],
                        [0, 1, 1],
                ]),
                np.array([
                        [0, 1],
                        [1, 1],
                        [1, 1]
                ]),
                np.array([
                        [1, 1, 0],
                        [1, 1, 1],
                ]),
                # mirrored below
                np.array([
                        [1, 1],
                        [1, 1],
                        [0, 1]
                ]),
                np.array([
                        [0, 1, 1],
                        [1, 1, 1],
                ]),
                np.array([
                        [1, 0],
                        [1, 1],
                        [1, 1]
                ]),
                np.array([
                        [1, 1, 1],
                        [1, 1, 0],
                ])
            ]

        self.__LARGE_CORNER = \
            [
                np.array([
                        [0, 0, 1],
                        [0, 0, 1],
                        [1, 1, 1]
                ]),
                np.array([
                        [1, 0, 0],
                        [1, 0, 0],
                        [1, 1, 1]
                ]),
                np.array([
                        [1, 1, 1],
                        [1, 0, 0],
                        [1, 0, 0]
                ]),
                np.array([
                        [1, 1, 1],
                        [0, 0, 1],
                        [0, 0, 1]
                ])
            ]

        self.__RIFLE = \
            [
                np.array([
                        [1, 1, 1, 1],
                        [0, 1, 0, 0]
                ]),
                np.array([
                        [0, 1],
                        [1, 1],
                        [0, 1],
                        [0, 1]
                ]),
                np.array([
                        [0, 0, 1, 0],
                        [1, 1, 1, 1]
                ]),
                np.array([
                        [1, 0],
                        [1, 0],
                        [1, 1],
                        [1, 0]
                ]),
                # mirrored below
                np.array([
                        [1, 1, 1, 1],
                        [0, 0, 1, 0]
                ]),
                np.array([
                        [0, 1],
                        [0, 1],
                        [1, 1],
                        [0, 1]
                ]),
                np.array([
                        [0, 1, 0, 0],
                        [1, 1, 1, 1]
                ]),
                np.array([
                        [1, 0],
                        [1, 1],
                        [1, 0],
                        [1, 0]
                ])
            ]

        self.__Z_SHAPE = \
            [
                np.array([
                        [1, 1, 0],
                        [0, 1, 1]
                ]),
                np.array([
                        [0, 1],
                        [1, 1],
                        [1, 0]
                ]),
                # mirrored below
                np.array([
                        [0, 1, 1],
                        [1, 1, 0]
                ]),
                np.array([
                        [1, 0],
                        [1, 1],
                        [0, 1]
                ])
            ]

        self.__STAIRS = \
            [
                np.array([
                        [0, 0, 1],
                        [0, 1, 1],
                        [1, 1, 0]
                ]),
                np.array([
                        [1, 0, 0],
                        [1, 1, 0],
                        [0, 1, 1]
                ]),
                np.array([
                        [0, 1, 1],
                        [1, 1, 0],
                        [1, 0, 0]
                ]),
                np.array([
                        [1, 1, 0],
                        [0, 1, 1],
                        [0, 0, 1]
                ])
            ]

        self.__CHAIR = \
            [
                np.array([
                        [1, 0],
                        [1, 0],
                        [1, 1],
                        [0, 1]
                ]),
                np.array([
                        [0, 1, 1, 1],
                        [1, 1, 0, 0]
                ]),
                np.array([
                        [1, 0],
                        [1, 1],
                        [0, 1],
                        [0, 1]
                ]),
                np.array([
                        [0, 0, 1, 1],
                        [1, 1, 1, 0]
                ]),
                # mirrored below
                np.array([
                        [0, 1],
                        [0, 1],
                        [1, 1],
                        [1, 0]
                ]),
                np.array([
                        [1, 1, 0, 0],
                        [0, 1, 1, 1]
                ]),
                np.array([
                        [0, 1],
                        [1, 1],
                        [1, 0],
                        [1, 0]
                ]),
                np.array([
                        [1, 1, 1, 0],
                        [0, 0, 1, 1]
                ])
            ]

        self.__C_SHAPE = \
            [
                np.array([
                        [1, 1],
                        [1, 0],
                        [1, 1]
                ]),
                np.array([
                        [1, 1, 1],
                        [1, 0, 1]
                ]),
                np.array([
                        [1, 1],
                        [0, 1],
                        [1, 1]
                ]),
                np.array([
                        [1, 0, 1],
                        [1, 1, 1]
                ])
            ]

        self.__TINY_CORNER = \
            [
                np.array([
                        [1, 0],
                        [1, 1]
                ]),
                np.array([
                        [1, 1],
                        [1, 0]
                ]),
                np.array([
                        [1, 1],
                        [0, 1]
                ]),
                np.array([
                        [0, 1],
                        [1, 1]
                ])
            ]

        self.__SQUARE = \
            [
                np.array([
                        [1, 1],
                        [1, 1]
                ])
            ]

        self.__PLUS = \
            [
                np.array([
                        [0, 1, 0],
                        [1, 1, 1],
                        [0, 1, 0]
                ])
            ]

        self.__LARGE_T = \
            [
                np.array([
                        [1, 1, 1],
                        [0, 1, 0],
                        [0, 1, 0]
                ]),
                np.array([
                        [0, 0, 1],
                        [1, 1, 1],
                        [0, 0, 1]
                ]),
                np.array([
                        [0, 1, 0],
                        [0, 1, 0],
                        [1, 1, 1]
                ]),
                np.array([
                        [1, 0, 0],
                        [1, 1, 1],
                        [1, 0, 0]
                ])
            ]

        self.__TINY_T = \
            [
                np.array([
                        [1, 1, 1],
                        [0, 1, 0]
                ]),
                np.array([
                        [0, 1],
                        [1, 1],
                        [0, 1]
                ]),
                np.array([
                        [0, 1, 0],
                        [1, 1, 1]
                ]),
                np.array([
                        [1, 0],
                        [1, 1],
                        [1, 0]
                ])
            ]

        self.__SHORT_L = \
            [
                np.array([
                        [1, 0],
                        [1, 0],
                        [1, 1]
                ]),
                np.array([
                        [1, 1, 1],
                        [1, 0, 0]
                ]),
                np.array([
                        [1, 1],
                        [0, 1],
                        [0, 1]
                ]),
                np.array([
                        [0, 0, 1],
                        [1, 1, 1]
                ]),
                # mirrored below
                np.array([
                        [0, 1],
                        [0, 1],
                        [1, 1]
                ]),
                np.array([
                        [1, 0, 0],
                        [1, 1, 1]
                ]),
                np.array([
                        [1, 1],
                        [1, 0],
                        [1, 0]
                ]),
                np.array([
                        [1, 1, 1],
                        [0, 0, 1]
                ])
            ]

        self.__TRIPLE = \
            [
                np.array([
                        [1],
                        [1],
                        [1]
                ]),
                np.array([
                        [1, 1, 1],
                ])
            ]

        self.__DUCK = \
            [
                np.array([
                        [0, 1, 0],
                        [0, 1, 1],
                        [1, 1, 0]
                ]),
                np.array([
                        [1, 0, 0],
                        [1, 1, 1],
                        [0, 1, 0]
                ]),
                np.array([
                        [0, 1, 1],
                        [1, 1, 0],
                        [0, 1, 0]
                ]),
                np.array([
                        [0, 1, 0],
                        [1, 1, 1],
                        [0, 0, 1]
                ]),
                # mirrored below
                np.array([
                        [0, 1, 0],
                        [1, 1, 0],
                        [0, 1, 1]
                ]),
                np.array([
                        [0, 1, 0],
                        [1, 1, 1],
                        [1, 0, 0]
                ]),
                np.array([
                        [1, 1, 0],
                        [0, 1, 1],
                        [0, 1, 0]
                ]),
                np.array([
                        [0, 0, 1],
                        [1, 1, 1],
                        [0, 1, 0]
                ])
            ]
        self.__names_of_initial_shapes = ['LONG_L', 'P_SHAPE', 'LARGE_CORNER', 'RIFLE']
        self.__list_of_all_shapes = [self.__LONG_L, self.__P_SHAPE, self.__LARGE_CORNER, self.__RIFLE, self.__Z_SHAPE,
                                     self.__STAIRS, self.__CHAIR, self.__C_SHAPE, self.__TINY_CORNER,self.__SQUARE,
                                     self.__PLUS,self.__LARGE_T, self.__TINY_T, self.__SHORT_L, self.__TRIPLE,
                                     self.__DUCK]
        self.__all_shapes_dict = {
            'LONG_L': self.__LONG_L,
            'P_SHAPE': self.__P_SHAPE,
            'LARGE_CORNER': self.__LARGE_CORNER,
            'RIFLE': self.__RIFLE,
            'Z_SHAPE': self.__Z_SHAPE,
            'STAIRS': self.__STAIRS,
            'CHAIR': self.__CHAIR,
            'C_SHAPE': self.__C_SHAPE,
            'TINY_CORNER': self.__TINY_CORNER,
            'SQUARE': self.__SQUARE,
            'PLUS': self.__PLUS,
            'LARGE_T': self.__LARGE_T,
            'TINY_T': self.__TINY_T,
            'SHORT_L': self.__SHORT_L,
            'TRIPLE': self.__TRIPLE,
            'DUCK': self.__DUCK
        }

    def get_names_of_initial_shapes(self):
        return copy.deepcopy(self.__names_of_initial_shapes)

    def get_all_shapes_dict(self):
        return copy.deepcopy(self.__all_shapes_dict)

    def get_max_possible_rotations(self) -> int:
        number_of_rotations_for_each_shape = [len(shape) for shape in self.__all_shapes_dict]
        return max(number_of_rotations_for_each_shape)
