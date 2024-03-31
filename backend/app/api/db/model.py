import dataclasses
import random
from typing import List, Final

import numpy as np


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
    
    def is_adjacent(self, another) -> bool:
        """
        selfを中心とする9マスの正方形の中にanotherが含まれるか
        """
        square_9: list[Vertex] = list()
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.y + 2):
                square_9.append(Vertex(x, y))
        for v in square_9:
            if v.x == another.x and v.y == another.y:
                return True
        return False


@dataclasses.dataclass
class Field:
    game_id: str
    num_mines: int
    width: int
    height: int
    squares: List[str]
    
    # クラス定数
    HIDDEN_MINE: Final[str] = '_X'
    FLAGGED_MINE: Final[str] = 'FX'
    X: Final[str] = 'X'
    
    def to_dict(self) -> dict:
        # TODO: vars()使えそうなのでto_dict()いらないかも
        return {
            'game_id': self.game_id,
            'num_mines': self.num_mines,
            'width': self.width,
            'height': self.height,
            'squares': self.squares,
        }
    
    @classmethod
    def from_dict(cls, d: dict) -> 'Field':
        return Field(
            game_id=d['game_id'],
            num_mines=d['num_mines'],
            width=d['width'],
            height=d['height'],
            squares=d['squares'],
        )
    
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
            if first_vertex.is_adjacent(Vertex(x=rand_x, y=rand_y)):
                continue
            if Vertex(rand_x, rand_y) in mines:
                continue
            mines.add(Vertex(x=rand_x, y=rand_y))
        
        # フィールドを初期化
        squares: list[str] = list()
        for i in range(x):
            for j in range(y):
                if Vertex(x=i, y=j) in mines:
                    squares.append(self.HIDDEN_MINE)
                    continue
                # 周囲の地雷の数を数える
                count: int = 0
                for k in range(i - 1, i + 2):
                    for l in range(j - 1, j + 2):
                        if not in_field(v=Vertex(k, l), width=self.width, height=self.height):
                            continue
                        elif Vertex(k, l) in mines:
                            count += 1
                squares.append(f'_{count}')
        
        self.squares = squares
    
    def flat(self, x: int, y: int) -> int:
        """
        2次元座標を1次元座標に変換する。
        """
        print(f'x: {x}, y: {y}, width: {self.width}, height: {self.height}')
        assert 0 <= x < self.width
        assert 0 <= y < self.height
        # TODO: イキってnp使ってるが、普通にself.width * y + xでいいかも
        return np.ravel_multi_index((y, x), (self.height, self.width))
    
    def dig(self, x: int, y: int) -> None:
        index: Final = self.flat(x, y)
        """
        マスを開けたあとの全マスの状況を返す。
        """
        # 地雷ならゲームオーバー
        if self.squares[index] == self.HIDDEN_MINE:
            self.squares[index] = self.X
            return
        
        # 該当のマスを開ける。0なら周囲を開く。
        self.__open_square(x, y)
        return
    
    def __open_square(self, x: int, y: int) -> None:
        x_y: Final = self.flat(x, y)
        if self.squares[x_y] == '_0':
            remaining_0: list[Vertex] = [Vertex(x, y)]
            while len(remaining_0) > 0:
                v = remaining_0.pop()
                # vの周囲8マスを開ける
                for i in range(v.x - 1, v.x + 2):
                    for j in range(v.y - 1, v.y + 2):
                        if not in_field(v=Vertex(i, j), width=self.width, height=self.height):
                            continue
                        i_j = self.flat(i, j)
                        if not self.squares[i_j].startswith('_'):
                            continue
                        elif self.squares[i_j] == '_0':
                            self.squares[i_j] = '0'
                            remaining_0.append(Vertex(i, j))
                        else:
                            self.squares[i_j] = self.squares[i_j][1]
        elif self.squares[x_y].startswith('_'):
            self.squares[x_y] = self.squares[x_y][1]
    
    def flag(self, x: int, y: int) -> None:
        """
        マスのフラグをON・OFFする。
        """
        index: Final = self.flat(x, y)
        if not len(self.squares[index]) == 2:
            return
        if self.is_game_ended():
            return
        if self.squares[index].startswith('F'):
            self.squares[index] = '_' + self.squares[index][1]
        else:
            self.squares[index] = 'F' + self.squares[index][1]
    
    def is_game_ended(self) -> bool:
        """
        ゲームが終了したかどうかを返す。
        """
        return self.is_game_cleared() or self.is_game_over()
    
    def is_game_cleared(self) -> bool:
        """
        ゲームクリアしたかどうかを返す。
        """
        for square in self.squares:
            if square.startswith('_'):
                return False
        return True
    
    def is_game_over(self) -> bool:
        """
        ゲームオーバーしたかどうかを返す。
        """
        for square in self.squares:
            if square == self.X:
                return True
        return False
    
    def masked_squares(self) -> list[str]:
        """
        クライアント向けにフィールドをマスクする。
        フラグが立っているマスはFに変換する。
        フラグ以外で開いてないマスは空文字列に変換する。
        ただし、地雷が開かれていてゲームオーバーの場合はマスクせずそのまま返す。
        """
        masked_squares: list[str] = list()
        for square in self.squares:
            if self.is_flagged(square):
                masked_squares.append('F')
            elif self.is_hidden(square):
                masked_squares.append('')
            elif square == self.X:
                return self.squares
            else:
                masked_squares.append(square)
        return masked_squares
    
    @classmethod
    def is_flagged(cls, square: str) -> bool:
        return square.startswith('F')
    
    @classmethod
    def is_hidden(cls, square: str) -> bool:
        return square.startswith('_')


def in_field(v: Vertex, width: int, height: int) -> bool:
    return 0 <= v.x < width and 0 <= v.y < height
