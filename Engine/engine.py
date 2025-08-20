from copy import deepcopy
from math import inf
from Board.board import Board
from Engine.board_evalation import evaluate
from MoveGeneration.move_generation import generate_moves
from Board.zobrist import compute_zobrist_hash, ZOBRIST_SIDE_KEY


_TT: dict[int, tuple[int, int, int]] = {}
# Tracks whether the last _negamax call returned directly from TT
_TT_HIT_USED: bool = False
# Transposition table entry format:
# key -> (stored_depth, flag, score)
# flag: 0 = exact, -1 = upper bound, 1 = lower bound


def _negamax(board: Board, depth: int, color: str, alpha: int, beta: int) -> int:
    """Alpha-beta negamax with a simple transposition table.

    Returns score from the perspective of `color`.
    """
    if depth == 0:
        return evaluate(board, color)

    opponent = "white" if color == "black" else "black"
    best_score = -inf

    # TT lookup (use incremental piece hash + side-to-move)
    key = board.zhash ^ (ZOBRIST_SIDE_KEY if color == 'black' else 0)
    if key in _TT:
        stored_depth, flag, stored_score = _TT[key]
        if stored_depth >= depth:
            if flag == 0:
                global _TT_HIT_USED
                _TT_HIT_USED = True
                return stored_score
            elif flag == -1 and stored_score <= alpha:
                _TT_HIT_USED = True
                return stored_score
            elif flag == 1 and stored_score >= beta:
                _TT_HIT_USED = True
                return stored_score

    possible_moves = generate_moves(board, color)
    if not possible_moves:
        # No legal moves; fall back to static eval (no checkmate detection here)
        return evaluate(board, color)

    for move in possible_moves:
        (from_rank, from_file), (to_rank, to_file) = move
        board_copy = deepcopy(board)
        board_copy.make_move(from_rank, from_file, to_rank, to_file)

        score = -_negamax(board_copy, depth - 1, opponent, -beta, -alpha)
        if score > best_score:
            best_score = score
        if best_score > alpha:
            alpha = best_score
        if alpha >= beta:
            break

    # TT store
    flag = 0
    if best_score <= alpha:
        flag = -1  # upper bound
    elif best_score >= beta:
        flag = 1   # lower bound
    _TT[key] = (depth, flag, best_score)

    return best_score


def get_best_move(board: Board, depth: int, color: str):
    """
    Return (best_move, best_score), where best_move is
    ((from_rank, from_file), (to_rank, to_file)) and best_score is from `color`'s perspective.
    """
    best_move = None
    best_score = -inf
    best_used_tt = False

    for move in generate_moves(board, color):
        (from_rank, from_file), (to_rank, to_file) = move
        board_copy = deepcopy(board)
        board_copy.make_move(from_rank, from_file, to_rank, to_file)
        # Reset TT-hit flag for this move
        global _TT_HIT_USED
        _TT_HIT_USED = False
        score = -_negamax(board_copy, depth - 1, "white" if color == "black" else "black", -inf, inf)
        if score > best_score:
            best_score = score
            best_move = move
            best_used_tt = _TT_HIT_USED

    return best_move, best_score, best_used_tt



    