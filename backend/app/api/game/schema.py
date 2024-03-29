from pydantic import BaseModel, PositiveInt, NonNegativeInt


class CreateGame(BaseModel):
    num_player: PositiveInt
    num_mines: PositiveInt
    x: PositiveInt
    y: PositiveInt
    
    model_config = {
        'json_schema_extra': {
            'example': {
                'num_player': 1,
                'num_mines': 10,
                'x': 10,
                'y': 10
            }
        }
    }


class PlayGame(BaseModel):
    x: NonNegativeInt
    y: NonNegativeInt


class FieldResult(BaseModel):
    squares: list[list[str]]
