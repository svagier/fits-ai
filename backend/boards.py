from enum import Enum


class Field(Enum):
    EMPTY = 0
    TAKEN = 1
    EXTRA_EMPTY = 2
    PLUS_1 = 3
    PLUS_2 = 4
    PLUS_3 = 5
    MINUS_5 = 6
    DOUBLE_GREEN = 7
    DOUBLE_BLUE = 8
    DOUBLE_ORANGE = 9
    DOUBLE_PINK = 10
    DOUBLE_PURPLE = 11


EMPTY = Field.EMPTY.value
EXTRA_EMPTY = Field.EXTRA_EMPTY.value

"""
Each Board is 12 Fields high and 6 Fields wide.
For each Board there are 3 rows of EXTRA_EMPTY. Blocks may be placed there, however neither negative nor positive 
points are given for filling EXTRA_EMPTY Fields. There are 3 rows of EXTRA_EMPTY, because the tallest Blocks (Shapes) in
the game are 4 Fields high, and there is no point in placing Block solely on EXTRA_EMPTY Fields (there will be no points
for that).
"""
BOARD_1 = \
    [
        [EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY],
        [EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY],
        [EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY, EXTRA_EMPTY],
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
    ]

