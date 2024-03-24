import dataclasses
from typing import List, Tuple, NamedTuple

from pydantic import BaseModel, PositiveInt


class CreateGame(BaseModel):
    num_player: PositiveInt
    num_mines: PositiveInt
    x: PositiveInt
    y: PositiveInt


class User(BaseModel):
    id: str
    display_name: str


@dataclasses.dataclass
class Game(BaseModel):
    game_id: str
    num_players: PositiveInt
    num_mines: PositiveInt
    created_by: str


class Vertex(NamedTuple):
    x: PositiveInt
    y: PositiveInt


@dataclasses.dataclass
class Field(BaseModel):
    game_id: str
    x: PositiveInt
    y: PositiveInt
    mines: List[Vertex]
    flags: List[Vertex]
    opens: List[Vertex]

