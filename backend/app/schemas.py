from typing import List, Tuple

from pydantic import BaseModel, PositiveInt


class CreateGame(BaseModel):
    num_player: int
    num_mines: int


class User(BaseModel):
    id: str
    display_name: str


class Game(BaseModel):
    id: str
    num_players: PositiveInt
    num_mines: PositiveInt
    created_by: str


class Vertex(BaseModel):
    x: PositiveInt
    y: PositiveInt


class Field(BaseModel):
    game_id: str
    x: PositiveInt
    y: PositiveInt
    mines: List[Vertex]
    flags: List[Vertex]
    opens: List[Vertex]

