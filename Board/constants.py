# Chess piece constants
# White pieces (uppercase)
WHITE_ROOK = 'R'
WHITE_KNIGHT = 'N'
WHITE_BISHOP = 'B'
WHITE_QUEEN = 'Q'
WHITE_KING = 'K'
WHITE_PAWN = 'P'

# Black pieces (lowercase)
BLACK_ROOK = 'r'
BLACK_KNIGHT = 'n'
BLACK_BISHOP = 'b'
BLACK_QUEEN = 'q'
BLACK_KING = 'k'
BLACK_PAWN = 'p'

# Empty square
EMPTY = ' '

# Board dimensions
BOARD_SIZE = 8
RANKS = 8
FILES = 8

# Starting position FEN (simplified)
STARTING_POSITION = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

# File labels (columns)
FILES_LABELS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

# Rank labels (rows)
RANKS_LABELS = ['8', '7', '6', '5', '4', '3', '2', '1']
