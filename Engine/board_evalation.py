from Board.board import Board
from Board.constants import EMPTY


def evaluate(board: Board, active_color: str):
    basic_score = basic_evaluation(board, active_color)
    return basic_score

def basic_evaluation(board: Board, active_color: str):
    piece_evaluation = {
        "P": 100,
        "N": 350,
        "B": 350,
        "R": 525,
        "Q": 1000,
        "K": 10000
    }
    score = 0
    for rank in board.board:
        for square in rank:
            if square != EMPTY:
                if (square.isupper() and active_color == "white") or (square.islower() and active_color == "black"):

                    score += piece_evaluation[square.upper()]
                else:
                    score -= piece_evaluation[square.upper()]
    return score


