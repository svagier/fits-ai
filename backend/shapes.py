import numpy as np
# ----------- start SHAPES -----------
"""
Each shape contains lists describing its rotations. Each next rotation of shape is rotated by 90 degrees clockwise
relative to the previous rotation. After all rotations for one 'side' of the Shape have been written in lists, next
lists describe the shape when it is 'turned over' (mirrored). Each mirrored rotation is also rotated by 90 degrees
clockwise. In other words, half of the subarrays will be for normal rotations of shape, half of the subarrays will be
for mirrored rotations.
It is possible for a shape not to have a mirrored versions (if it is rotationally symmetric or if mirrored rotations
are the same as original rotations).
"""
LONG_L = \
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

P_SHAPE = \
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

LARGE_CORNER = \
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

RIFLE = \
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

Z_SHAPE = \
    [
        np.array([
                [1, 1, 0],
                [0, 1, 1]
        ]),
        np.array([
                [0, 1],
                [1, 1],
                [1, 0]
        ])
    ]

STAIRS = \
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

CHAIR = \
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

C_SHAPE = \
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

TINY_CORNER = \
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

SQUARE = \
    [
        np.array([
                [1, 1],
                [1, 1]
        ])
    ]

PLUS = \
    [
        np.array([
                [0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]
        ])
    ]

LARGE_T = \
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

TINY_T = \
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

SHORT_L = \
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

TRIPLE = \
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

DUCK = \
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
#TODO specify numpy dtype?

INITIAL_SHAPES = [LONG_L, P_SHAPE, LARGE_CORNER, RIFLE]
ALL_SHAPES = [LONG_L, P_SHAPE, LARGE_CORNER, RIFLE, Z_SHAPE, STAIRS, CHAIR, C_SHAPE, TINY_CORNER, SQUARE, PLUS, LARGE_T,
              TINY_T, SHORT_L, TRIPLE, DUCK]
