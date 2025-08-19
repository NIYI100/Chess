from copy import deepcopy
from math import inf
from Board.board import Board
from Engine.board_evalation import evaluate
from MoveGeneration.move_generation import generate_moves


def _negamax(board: Board, depth: int, color: str, alpha: int, beta: int) -> int:
    """Alpha-beta negamax. Returns score from the perspective of `color`."""
    if depth == 0:
        return evaluate(board, color)

    opponent = "white" if color == "black" else "black"
    best_score = -inf

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

    return best_score


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
        score = -_negamax(board_copy, depth - 1, "white" if color == "black" else "black", -inf, inf)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move, best_score



    