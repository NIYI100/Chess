from .constants import *
from .zobrist import compute_piece_hash, PIECE_TO_INDEX, ZOBRIST_PIECE_KEYS

class Board:
    def __init__(self, position=None):
        """
        Initialize the chess board.
        Args:
            position: Optional starting position (2D list). If None, uses standard starting position.
        """
        if position is None:
            self.board = [row[:] for row in STARTING_POSITION]
        else:
            self.board = [row[:] for row in position]
        # Incremental Zobrist piece-hash (excludes side-to-move)
        self.zhash: int = compute_piece_hash(self)
    
    def get_piece(self, rank, file):
        """
        Get piece at specified position.
        Args:
            rank: Row index (0-7, where 0 is top rank)
            file: Column index (0-7, where 0 is leftmost file)
        Returns:
            Piece character or empty string
        """
        if 0 <= rank < BOARD_SIZE and 0 <= file < BOARD_SIZE:
            return self.board[rank][file]
        return None
    
    def set_piece(self, rank, file, piece):
        """
        Set piece at specified position.
        Args:
            rank: Row index (0-7)
            file: Column index (0-7)
            piece: Piece character to place
        Returns:
            True if successful, False otherwise
        """
        if 0 <= rank < BOARD_SIZE and 0 <= file < BOARD_SIZE:
            self.board[rank][file] = piece
            return True
        return False
    
    def is_white_piece(self, piece):
        """Check if piece is white (uppercase)."""
        return piece.isupper() and piece != EMPTY
    
    def is_black_piece(self, piece):
        """Check if piece is black (lowercase)."""
        return piece.islower() and piece != EMPTY
    
    def is_empty(self, rank, file):
        """Check if square is empty."""
        return self.get_piece(rank, file) == EMPTY
    
    def get_piece_type(self, piece):
        """Get the type of piece (ignoring color)."""
        if piece == EMPTY:
            return None
        return piece.upper()
    
    def display(self):
        """Display the chess board with coordinates."""
        # Display file labels centered above columns
        file_header = "  "
        for file in range(BOARD_SIZE):
            file_header += f"  {FILES_LABELS[file]} "
        print(file_header)
        print("  " + "-" * 33)
        
        for rank in range(BOARD_SIZE):
            row_display = f"{RANKS_LABELS[rank]} |"
            for file in range(BOARD_SIZE):
                piece = self.board[rank][file]
                row_display += f" {piece} |"
            print(row_display)
            if rank < BOARD_SIZE - 1:
                print("  " + "-" * 33)
        
        print("  " + "-" * 33)
        # Display file labels centered below columns
        print(file_header)
    
    def get_fen(self):
        """Convert board to FEN notation (simplified)."""
        fen_parts = []
        
        for rank in range(BOARD_SIZE):
            rank_str = ""
            empty_count = 0
            
            for file in range(BOARD_SIZE):
                piece = self.board[rank][file]
                if piece == EMPTY:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        rank_str += str(empty_count)
                        empty_count = 0
                    rank_str += piece
            
            if empty_count > 0:
                rank_str += str(empty_count)
            
            fen_parts.append(rank_str)
        
        return "/".join(fen_parts)
    
    def reset_to_starting_position(self):
        """Reset board to standard starting position."""
        self.board = [row[:] for row in STARTING_POSITION]
    
    def make_move(self, from_rank, from_file, to_rank, to_file):
        """
        Make a move on the board.
        Args:
            from_rank, from_file: Source position
            to_rank, to_file: Destination position
        Returns:
            True if move was successful, False otherwise
        """
        # Basic validation
        if not (0 <= from_rank < BOARD_SIZE and 0 <= from_file < BOARD_SIZE and
                0 <= to_rank < BOARD_SIZE and 0 <= to_file < BOARD_SIZE):
            return False
        
        # Get the piece to move
        piece = self.get_piece(from_rank, from_file)
        if piece == EMPTY:
            return False
        
        # Incremental Zobrist update: remove moving piece from source, toggle piece at dest
        from_sq = from_rank * BOARD_SIZE + from_file
        to_sq = to_rank * BOARD_SIZE + to_file
        moving_index = PIECE_TO_INDEX[piece]

        # If capturing, remove captured piece at destination from hash first
        captured = self.board[to_rank][to_file]
        if captured != EMPTY:
            self.zhash ^= ZOBRIST_PIECE_KEYS[PIECE_TO_INDEX[captured]][to_sq]

        # Remove piece from source
        self.zhash ^= ZOBRIST_PIECE_KEYS[moving_index][from_sq]
        # Add piece to destination
        self.zhash ^= ZOBRIST_PIECE_KEYS[moving_index][to_sq]

        # Make the move on the board
        self.board[to_rank][to_file] = piece
        self.board[from_rank][from_file] = EMPTY
        
        return True
    
    def get_all_pieces(self, color='white'):
        """
        Get all pieces of a specific color.
        Args:
            color: 'white' or 'black'
        Returns:
            List of tuples (rank, file, piece)
        """
        pieces = []
        for rank in range(BOARD_SIZE):
            for file in range(BOARD_SIZE):
                piece = self.board[rank][file]
                if piece != EMPTY:
                    if color == 'white' and self.is_white_piece(piece):
                        pieces.append((rank, file, piece))
                    elif color == 'black' and self.is_black_piece(piece):
                        pieces.append((rank, file, piece))
        return pieces