# Chess Board Implementation

A simple chess board implementation in Python using string notation for chess pieces.

## Piece Notation

The chess pieces are represented using the following string notation:

### White Pieces (Uppercase)
- `R` - White Rook
- `N` - White Knight  
- `B` - White Bishop
- `Q` - White Queen
- `K` - White King
- `P` - White Pawn

### Black Pieces (Lowercase)
- `r` - Black Rook
- `n` - Black Knight
- `b` - Black Bishop
- `q` - Black Queen
- `k` - Black King
- `p` - Black Pawn

### Empty Squares
- ` ` (space) - Empty square

## Features

- 8x8 chess board representation
- Standard starting position
- Piece movement and placement
- Board display with coordinates
- FEN notation support
- Piece color and type identification
- Custom position support

## Usage

### Basic Usage

```python
from Board.board import Board

# Create a new board with standard starting position
board = Board()

# Display the board
board.display()

# Get a piece at a specific position
piece = board.get_piece(6, 4)  # e2 (rank 6, file 4)
print(f"Piece at e2: {piece}")  # Output: P (white pawn)

# Make a move
board.make_move(6, 4, 4, 4)  # Move pawn from e2 to e4
```

### Working with Pieces

```python
# Check piece properties
piece = board.get_piece(0, 0)
print(board.is_white_piece(piece))  # False (black rook)
print(board.is_black_piece(piece))  # True
print(board.get_piece_type(piece))  # R (rook type)

# Get all pieces of a color
white_pieces = board.get_all_pieces('white')
for rank, file, piece in white_pieces:
    print(f"{piece} at rank {rank}, file {file}")
```

### Custom Positions

```python
# Create a custom board position
custom_position = [
    [' ', ' ', ' ', ' ', 'k', ' ', ' ', ' '],  # Black king at e8
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', 'K', ' ', ' ', ' ']   # White king at e1
]

custom_board = Board(custom_position)
custom_board.display()
```

## Board Coordinates

The board uses 0-based indexing:
- **Ranks** (rows): 0-7 (0 = top rank, 7 = bottom rank)
- **Files** (columns): 0-7 (0 = leftmost file, 7 = rightmost file)

Standard chess notation mapping:
- a1 = (7, 0)
- e4 = (4, 4)  
- h8 = (0, 7)

## Running the Example

```bash
python example_usage.py
```

This will demonstrate various features of the chess board implementation.

## File Structure

```
Chess/
├── Board/
│   ├── __init__.py      # Module initialization
│   ├── constants.py     # Chess piece constants and board setup
│   └── board.py         # Main Board class implementation
├── example_usage.py     # Example usage script
└── README.md           # This file
```

## Future Enhancements

- Move validation rules
- Check/checkmate detection
- Game state management
- Move history
- Algebraic notation support
- GUI interface

