from Board.board import Board
from Board.constants import BOARD_SIZE, WHITE_PAWN, WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN, WHITE_KING
from Board.constants import BLACK_PAWN, BLACK_ROOK, BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN, BLACK_KING, EMPTY


def generate_moves(board: Board, color: str):
    """Generate all legal moves for a given color"""
    moves = []
    for rank in range(BOARD_SIZE):
        for file in range(BOARD_SIZE):
            piece = board.board[rank][file]
            if piece != EMPTY and piece.isupper() == (color == 'white'):
                piece_moves = calculate_legal_moves(board, (rank, file))
                moves.extend(piece_moves)
    return moves


def calculate_legal_moves(board: Board, from_square: tuple[int, int]):
    """Calculate legal moves for a piece at a given square"""
    from_rank, from_file = from_square
    piece = board.board[from_rank][from_file]
    
    if piece == EMPTY:
        return []
    
    # Determine piece type (case-insensitive)
    piece_type = piece.upper()
    
    # Dictionary mapping piece types to their move generation functions
    piece_move_functions = {
        'P': generate_pawn_moves,
        'R': generate_rook_moves,
        'N': generate_knight_moves,
        'B': generate_bishop_moves,
        'Q': generate_queen_moves,
        'K': generate_king_moves
    }
    
    # Dynamically call the appropriate function
    if piece_type in piece_move_functions:
        return piece_move_functions[piece_type](board, from_square)
    else:
        return []


def generate_pawn_moves(board: Board, from_square: tuple[int, int]):
    """Generate moves for a pawn"""
    from_rank, from_file = from_square
    piece = board.board[from_rank][from_file]
    is_white = piece.isupper()
    moves = []
    
    # Direction: white pawns move up (decreasing rank), black pawns move down (increasing rank)
    direction = -1 if is_white else 1
    start_rank = 6 if is_white else 1
    
    # Forward move
    new_rank = from_rank + direction
    if 0 <= new_rank < BOARD_SIZE and board.board[new_rank][from_file] == EMPTY:
        moves.append((from_square, (new_rank, from_file)))
        
        # Double move from starting position
        if from_rank == start_rank:
            new_rank2 = new_rank + direction
            if 0 <= new_rank2 < BOARD_SIZE and board.board[new_rank2][from_file] == EMPTY:
                moves.append((from_square, (new_rank2, from_file)))
    
    # Captures (diagonal)
    for file_offset in [-1, 1]:
        new_file = from_file + file_offset
        new_rank = from_rank + direction
        if (0 <= new_rank < BOARD_SIZE and 0 <= new_file < BOARD_SIZE):
            target_piece = board.board[new_rank][new_file]
            if target_piece != EMPTY and target_piece.isupper() != is_white:
                moves.append((from_square, (new_rank, new_file)))
    
    #TODO: En passant
    return moves


def generate_rook_moves(board: Board, from_square: tuple[int, int]):
    """Generate moves for a rook"""
    from_rank, from_file = from_square
    piece = board.board[from_rank][from_file]
    is_white = piece.isupper()
    moves = []
    
    # Rook moves in straight lines (horizontal and vertical)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
    
    for d_rank, d_file in directions:
        for step in range(1, BOARD_SIZE):
            new_rank = from_rank + step * d_rank
            new_file = from_file + step * d_file
            
            if not (0 <= new_rank < BOARD_SIZE and 0 <= new_file < BOARD_SIZE):
                break
                
            target_piece = board.board[new_rank][new_file]
            if target_piece == EMPTY:
                moves.append((from_square, (new_rank, new_file)))
            elif target_piece.isupper() != is_white:
                moves.append((from_square, (new_rank, new_file)))
                break
            else:
                break  # Own piece blocking
    
    return moves


def generate_knight_moves(board: Board, from_square: tuple[int, int]):
    """Generate moves for a knight"""
    from_rank, from_file = from_square
    piece = board.board[from_rank][from_file]
    is_white = piece.isupper()
    moves = []
    
    # Knight moves in L-shape
    knight_moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]
    
    for d_rank, d_file in knight_moves:
        new_rank = from_rank + d_rank
        new_file = from_file + d_file
        
        if 0 <= new_rank < BOARD_SIZE and 0 <= new_file < BOARD_SIZE:
            target_piece = board.board[new_rank][new_file]
            if target_piece == EMPTY or target_piece.isupper() != is_white:
                moves.append((from_square, (new_rank, new_file)))
    
    return moves


def generate_bishop_moves(board: Board, from_square: tuple[int, int]):
    """Generate moves for a bishop"""
    from_rank, from_file = from_square
    piece = board.board[from_rank][from_file]
    is_white = piece.isupper()
    moves = []
    
    # Bishop moves diagonally
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    for d_rank, d_file in directions:
        for step in range(1, BOARD_SIZE):
            new_rank = from_rank + step * d_rank
            new_file = from_file + step * d_file
            
            if not (0 <= new_rank < BOARD_SIZE and 0 <= new_file < BOARD_SIZE):
                break
                
            target_piece = board.board[new_rank][new_file]
            if target_piece == EMPTY:
                moves.append((from_square, (new_rank, new_file)))
            elif target_piece.isupper() != is_white:
                moves.append((from_square, (new_rank, new_file)))
                break
            else:
                break  # Own piece blocking
    
    return moves


def generate_queen_moves(board: Board, from_square: tuple[int, int]):
    """Generate moves for a queen (combination of rook and bishop)"""
    # Queen combines rook and bishop moves
    rook_moves = generate_rook_moves(board, from_square)
    bishop_moves = generate_bishop_moves(board, from_square)
    return rook_moves + bishop_moves


def generate_king_moves(board: Board, from_square: tuple[int, int]):
    """Generate moves for a king"""
    from_rank, from_file = from_square
    piece = board.board[from_rank][from_file]
    is_white = piece.isupper()
    moves = []
    
    # King moves one square in any direction
    king_moves = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    for d_rank, d_file in king_moves:
        new_rank = from_rank + d_rank
        new_file = from_file + d_file
        
        if 0 <= new_rank < BOARD_SIZE and 0 <= new_file < BOARD_SIZE:
            target_piece = board.board[new_rank][new_file]
            if target_piece == EMPTY or target_piece.isupper() != is_white:
                moves.append((from_square, (new_rank, new_file)))
    
    return moves

    
