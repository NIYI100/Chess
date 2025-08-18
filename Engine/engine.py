from copy import deepcopy
from math import inf
from Board.board import Board
from Engine.board_evalation import evaluate
from MoveGeneration.move_generation import generate_moves


def lookahead(board: Board, depth: int, color: str):
    return miniMax(board, depth, color, - inf, inf)

def miniMax(board: Board, depth: int, color: str, alpha: int, beta: int):
    if depth ==0:
        return evaluate(board, color)
    # if GAME IS OVER
    maxAlpha : int = alpha
    possible_moves = generate_moves(board, color)
    board_copy =deepcopy(board)
    new_active_color = "white" if color == "black" else "black"
    for move in possible_moves:
        board_copy.make_move(move)
        score = -miniMax(board_copy, depth - 1, color, new_active_color, -beta, -maxAlpha)
        if score > maxAlpha:
            maxAlpha = score
        if maxAlpha >= beta:
            break
    return maxAlpha



    