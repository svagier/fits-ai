from enum import Enum


class Field(Enum):
    EMPTY = 0
    TAKEN = 1
    EXTRA_EMPTY = 2
    PLUS_1 = 3
    PLUS_2 = 4
    PLUS_3 = 5
    MINUS_5 = 6
    PAIR_1 = 7
    PAIR_2 = 8
    PAIR_3 = 9
    PAIR_4 = 10
    PAIR_5 = 11


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

