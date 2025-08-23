from dataclasses import dataclass
from enum import Enum


class NodeType(Enum):
    EXACT = 0
    LOWER_BOUND = 1
    UPPER_BOUND = 2

@dataclass
class TTEntry:
    depth: int
    value: int
    flag: NodeType
    best_move: tuple[tuple[int, int], tuple[int, int]]

tt_table = {}