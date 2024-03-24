import random
from typing import Tuple

from pydantic import PositiveInt

from app.schemas import Vertex


def init_field(
        x: PositiveInt,
        y: PositiveInt,
        num_mines: PositiveInt
) -> list[Vertex]:
    """マインスイーパーのフィールドに地雷を配置する。"""
    if not 0 <= num_mines <= x*y:
        raise ValueError("地雷の数が多すぎる")
    
    mines: set[Vertex] = set()  # setを使うことで重複を防ぐ
    while len(mines) < num_mines:
        x = random.randint(0, x-1)
        y = random.randint(0, y-1)
        mines.add(Vertex(x=x, y=y))
    
    return list(mines)
 
