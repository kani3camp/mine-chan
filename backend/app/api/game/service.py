import random
from typing import Tuple, List

from pydantic import PositiveInt

from app.api.game.model import Vertex




def is_adjacent(v1: Vertex, v2: Vertex) -> bool:
    """
    v1を中心とする9マスの正方形の中にv2が含まれるか
    """
    square_9: list[Vertex] = list()
    for x in range(v1.x -1, v1.x + 2):
        for y in range(v1.y - 1, v1.y + 2):
            square_9.append(Vertex(x, y))
    for v in square_9:
        if v.x == v2.x and v.y == v2.y:
            return True
    return False


def in_field(v: Vertex, x: int, y: int) -> bool:
    return 0 <= v.x < x and 0 <= v.y < y


