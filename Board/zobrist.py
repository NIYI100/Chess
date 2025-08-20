from __future__ import annotations

import random
from typing import Dict, List

from .constants import BOARD_SIZE, EMPTY


# Piece-to-index mapping for Zobrist keys (12 piece types)
PIECE_TO_INDEX: Dict[str, int] = {
    'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,
    'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11,
}


def _init_zobrist_keys(seed: int = 123456789) -> tuple[List[List[int]], int]:
    rng = random.Random(seed)
    piece_keys: List[List[int]] = [[0] * (BOARD_SIZE * BOARD_SIZE) for _ in range(12)]
    for piece_index in range(12):
        for sq in range(BOARD_SIZE * BOARD_SIZE):
            piece_keys[piece_index][sq] = rng.getrandbits(64)
    side_key = rng.getrandbits(64)
    return piece_keys, side_key


ZOBRIST_PIECE_KEYS, ZOBRIST_SIDE_KEY = _init_zobrist_keys()


def compute_zobrist_hash(board, side_to_move: str) -> int:
    """Compute Zobrist hash for the given board and side to move.

    This recomputes the hash from scratch; for performance, you can cache it in the board
    and update incrementally when making moves.
    """
    h: int = 0
    for rank in range(BOARD_SIZE):
        for file in range(BOARD_SIZE):
            piece = board.board[rank][file]
            if piece != EMPTY:
                piece_index = PIECE_TO_INDEX[piece]
                sq_index = rank * BOARD_SIZE + file
                h ^= ZOBRIST_PIECE_KEYS[piece_index][sq_index]

    if side_to_move == 'black':
        h ^= ZOBRIST_SIDE_KEY
    return h


def compute_piece_hash(board) -> int:
    """Compute Zobrist hash for pieces only (no side-to-move)."""
    h: int = 0
    for rank in range(BOARD_SIZE):
        for file in range(BOARD_SIZE):
            piece = board.board[rank][file]
            if piece != EMPTY:
                piece_index = PIECE_TO_INDEX[piece]
                sq_index = rank * BOARD_SIZE + file
                h ^= ZOBRIST_PIECE_KEYS[piece_index][sq_index]
    return h


