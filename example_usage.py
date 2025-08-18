#!/usr/bin/env python3
"""
Example usage of the Chess Board implementation.
This script demonstrates how to create, display, and manipulate the chess board.
"""

from Board.board import Board
from Board.constants import *

def main():
    print("=== Chess Board Implementation Example ===\n")
    
    # Create a new board with standard starting position
    board = Board()
    
    print("1. Standard starting position:")
    board.display()
    print()
    
    # Show FEN notation
    print("2. FEN notation:")
    print(board.get_fen())
    print()
    
    # Make some moves
    print("3. Making moves:")
    
    # Move white pawn from e2 to e4
    print("Moving white pawn from e2 (rank 6, file 4) to e4 (rank 4, file 4)")
    board.make_move(6, 4, 4, 4)  # e2 to e4
    board.display()
    print()
    
    # Move black pawn from e7 to e5
    print("Moving black pawn from e7 (rank 1, file 4) to e5 (rank 3, file 4)")
    board.make_move(1, 4, 3, 4)  # e7 to e5
    board.display()
    print()
    
    # Show current FEN
    print("4. Current FEN notation:")
    print(board.get_fen())
    print()
    
    # Demonstrate piece identification
    print("5. Piece identification:")
    piece = board.get_piece(4, 4)  # e4
    print(f"Piece at e4: '{piece}'")
    print(f"Is white piece: {board.is_white_piece(piece)}")
    print(f"Is black piece: {board.is_black_piece(piece)}")
    print(f"Piece type: {board.get_piece_type(piece)}")
    print()
    
    # Show all white pieces
    print("6. All white pieces:")
    white_pieces = board.get_all_pieces('white')
    for rank, file, piece in white_pieces:
        file_label = FILES_LABELS[file]
        rank_label = RANKS_LABELS[rank]
        print(f"{piece} at {file_label}{rank_label}")
    print()
    
    # Reset to starting position
    print("7. Resetting to starting position:")
    board.reset_to_starting_position()
    board.display()
    print()
    
    # Demonstrate custom position
    print("8. Creating custom position:")
    custom_position = [
        [' ', ' ', ' ', ' ', 'k', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', 'K', ' ', ' ', ' ']
    ]
    custom_board = Board(custom_position)
    custom_board.display()
    print("This represents a king vs king endgame!")

if __name__ == "__main__":
    main()
