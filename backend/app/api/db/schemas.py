from typing import List

from pydantic import BaseModel


class GameBase(BaseModel):
    num_players: int
    num_mines: int

class GameCreate(GameBase):
    num_players: int
    num_mines: int

class Game(GameBase):
    id: int

    class Config:
        orm_mode = True


class FieldBase(BaseModel):
    num_mines: int
    width: int
    height: int
    squares: List[str]

class FieldCreate(FieldBase):
    game_id: int
    num_mines: int
    width: int
    height: int
    squares: List[str]

class Field(FieldBase):
    class Config:
        orm_mode = True
