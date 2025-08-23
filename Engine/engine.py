from copy import deepcopy
from math import inf
from Board.board import Board
from Engine.board_evalation import evaluate
from MoveGeneration.move_generation import generate_moves
from Engine.transpositional_table.zobrist import ZOBRIST_SIDE_KEY
from Engine.transpositional_table import tt_table, NodeType, TTEntry


def _negamax(board: Board, depth: int, color: str, alpha: int, beta: int) -> int:
    """Alpha-beta negamax with a simple transposition table.

    Returns score from the perspective of `color`.
    """
    opponent = "white" if color == "black" else "black"
    best_score = -inf

    # TT lookup (use incremental piece hash + side-to-move)
    key = board.zhash ^ (ZOBRIST_SIDE_KEY if color == 'black' else 0)
    if key in tt_table:
        entry = tt_table[key]

        if entry.depth >= depth:
            if entry.flag == NodeType.EXACT:
                print(f"TT hit: {entry.value}")
                return entry.value, entry.best_move
            elif entry.flag == NodeType.LOWER_BOUND:
                alpha = max(alpha, entry.value)
            elif entry.flag == NodeType.UPPER_BOUND:
                beta = min(beta, entry.value)

            if alpha >= beta:
                print(f"TT alpha >= beta: {entry.value}")
                return entry.value, entry.best_move

    if depth == 0:
        return evaluate(board, color), None


    best_move = None
    possible_moves = generate_moves(board, color)


    if not possible_moves:
        # No legal moves; fall back to static eval (no checkmate detection here)
        return evaluate(board, color), None

    for move in possible_moves:
        (from_rank, from_file), (to_rank, to_file) = move
        board_copy = deepcopy(board)
        board_copy.make_move(from_rank, from_file, to_rank, to_file)

        child_score, _ = _negamax(board_copy, depth - 1, opponent, -beta, -alpha)
        score = -child_score
        if score > best_score:
            best_score = score
            best_move = move  # Keep the original move that led to this position
        if best_score > alpha:
            alpha = best_score
        if alpha >= beta:
            break


    if best_score <= alpha:
        flag = NodeType.UPPER_BOUND
    elif best_score >= beta:
        flag = NodeType.LOWER_BOUND
    else:
        flag = NodeType.EXACT

    new_entry = TTEntry(depth=depth, value=best_score, flag=flag, best_move=best_move)
    tt_table[key] = new_entry
    print(f"TT stored: {best_score}")

    return best_score, best_move


def get_best_move(board: Board, depth: int, color: str):
    """
    Return (best_move, best_score), where best_move is
    ((from_rank, from_file), (to_rank, to_file)) and best_score is from `color`'s perspective.
    """
    best_move = None
    best_score = -inf

    for move in generate_moves(board, color):
        (from_rank, from_file), (to_rank, to_file) = move
        board_copy = deepcopy(board)
        board_copy.make_move(from_rank, from_file, to_rank, to_file)
        child_score, _ = _negamax(board_copy, depth - 1, "white" if color == "black" else "black", -inf, inf)
        score = -child_score
        if score > best_score:
            best_score = score
            best_move = move

    return best_score, best_move



    