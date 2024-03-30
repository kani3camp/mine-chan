import dataclasses
import random
from typing import List, Final

from .schema import FieldResult


@dataclasses.dataclass
class Game:
    game_id: str
    num_players: int
    num_mines: int
    created_by: str


@dataclasses.dataclass
class Vertex:
    x: int
    y: int
    
    def __hash__(self):
        return hash(self.x) + hash(self.y)
    
    def to_dict(self) -> dict[str, int]:
        return {
            'x': self.x,
            'y': self.y
        }
    
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y


@dataclasses.dataclass
class Field:
    game_id: str
    num_mines: int
    x: int
    y: int
    mines: List[Vertex]
    flags: List[Vertex]
    opens: List[Vertex]
    
    # クラス定数
    HIDDEN_MINE: Final[str] = '_x_'
    
    def to_dict(self) -> dict:
        return {
            'game_id': self.game_id,
            'x': self.x,
            'y': self.y,
            'mines': [v.to_dict() for v in self.mines],
            'flags': [v.to_dict() for v in self.flags],
            'opens': [v.to_dict() for v in self.opens],
        }
    
    def init_mines(
            self,
            x: int,
            y: int,
            num_mines: int,
            first_vertex: Vertex,
    ) -> None:
        """マインスイーパーのフィールドに地雷を配置する。"""
        if not 0 <= num_mines <= x * y:
            raise ValueError("地雷の数が多すぎる")
        
        mines: set[Vertex] = set()  # setを使うことで重複を防ぐ
        while len(mines) < num_mines:
            rand_x = random.randint(0, x - 1)
            rand_y = random.randint(0, y - 1)
            if is_adjacent(Vertex(rand_x, rand_y), first_vertex):
                continue
            if Vertex(rand_x, rand_y) in mines:
                continue
            mines.add(Vertex(x=rand_x, y=rand_y))
        
        self.mines = list(mines)
    
    def dig(self, x: int, y: int) -> FieldResult:
        """
        マスを開けたあとの全マスの状況を返す。
        """
        # 地雷ならゲームオーバーなので、未開の部分も含めて全部表示
        if Vertex(x, y) in self.mines:
            # 未開部分は異なる表記（地雷：'_x_', 数字: '_0_'など）
            pass
        # 0ならば数字に囲まれた範囲を表示
        # 1以上ならそのマスだけ表示
        
        # もし残りが地雷でない未開部分だけになったらゲームクリア


def is_adjacent(v1: Vertex, v2: Vertex) -> bool:
    """
    v1を中心とする9マスの正方形の中にv2が含まれるか
    """
    square_9: list[Vertex] = list()
    for x in range(v1.x - 1, v1.x + 2):
        for y in range(v1.y - 1, v1.y + 2):
            square_9.append(Vertex(x, y))
    for v in square_9:
        if v.x == v2.x and v.y == v2.y:
            return True
    return False


def in_field(v: Vertex, x: int, y: int) -> bool:
    return 0 <= v.x < x and 0 <= v.y < y
