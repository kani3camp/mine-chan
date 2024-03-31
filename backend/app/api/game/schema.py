from pydantic import BaseModel, PositiveInt, NonNegativeInt, Field

from app.api.db.model import GameStateEnum


class CreateGame(BaseModel):
    num_player: PositiveInt = Field(description='プレイヤー数')
    num_mines: PositiveInt = Field(description='地雷の数')
    x: PositiveInt = Field(description='x軸の長さ')
    y: PositiveInt = Field(description='y軸の長さ')
    
    model_config = {
        'json_schema_extra': {
            'example': {
                'num_player': 1,
                'num_mines': 10,
                'x': 9,
                'y': 9
            }
        }
    }


class DigSquare(BaseModel):
    x: NonNegativeInt = Field(description='0始まりのx座標')
    y: NonNegativeInt = Field(description='0始まりのy座標')


class FlagSquare(BaseModel):
    x: NonNegativeInt = Field(description='0始まりのx座標')
    y: NonNegativeInt = Field(description='0始まりのy座標')


class FieldResult(BaseModel):
    squares: list[str] = ...
    game_state: GameStateEnum = ...
    mines_left: NonNegativeInt = Field(description='残り地雷数')
