from .schema import CreateGame, DigSquare, FieldResult, FlagSquare
from ..db.model import Game, Field, Vertex
from ..db import db
from ..db.redis import r, read_games, push_game, set_field, read_field
from ..db.model import in_field

from fastapi import APIRouter, HTTPException

game_router = APIRouter(prefix='/game', tags=['game'])


@game_router.get('/', name='ゲーム一覧を取得する')
async def get_games() -> list[str]:
    games = await read_games()
    return games


@game_router.get("/{game_id}", name='ゲームを取得する')
async def get_game(game_id: str) -> FieldResult:
    field = await read_field(game_id)
    if field is None:
        raise HTTPException(status_code=404)
    masked_squares = field.masked_squares()
    return FieldResult(squares=masked_squares)


@game_router.post("/", name='ゲームを作成する')
async def create_game(request: CreateGame) -> str:
    new_game_ref = db.games_collection.document()
    game = Game(
        game_id=new_game_ref.id,
        num_players=request.num_player,
        num_mines=request.num_mines,
        created_by=''
    )
    await new_game_ref.set(vars(game))
    
    # フィールドを作成（初期化）
    field = Field(
        game_id=new_game_ref.id,
        num_mines=request.num_mines,
        width=request.x,
        height=request.y,
        squares=[''] * request.x * request.y,
    )
    
    # 地雷を配置
    await db.write_field(field.to_dict())
    await set_field(new_game_ref.id, field)
    await push_game(new_game_ref.id)
    
    return new_game_ref.id


@game_router.post("/{game_id}/dig", name='マスを開ける')
async def dig(game_id: str, request: DigSquare) -> FieldResult:
    field: Field | None = await read_field(game_id=game_id)
    if field is None:
        raise HTTPException(status_code=404)
    if field.squares == [''] * field.width * field.height:
        field.init_mines(x=field.width, y=field.height, num_mines=field.num_mines, first_vertex=Vertex(request.x, request.y))
    
    if not in_field(
            v=Vertex(request.x, request.y),
            width=field.width,
            height=field.height):
        raise HTTPException(status_code=400, detail='無効なマスです')
    
    field.dig(x=request.x, y=request.y)
    await set_field(game_id, field)
    
    masked_squares = field.masked_squares()
    
    return FieldResult(squares=masked_squares)


@game_router.post("/{game_id}/flag", name='フラグをON/OFFする')
async def flag(game_id: str, request: FlagSquare) -> FieldResult:
    field: Field | None = await read_field(game_id=game_id)
    if field is None:
        raise HTTPException(status_code=404)
    if len(field.squares) == 0:
        raise HTTPException(status_code=400, detail='まずは１箇所マスを開けてください')
    
    if not in_field(
            v=Vertex(request.x, request.y),
            width=field.width,
            height=field.height):
        raise HTTPException(status_code=400, detail='無効なマスです')
    
    field.flag(x=request.x, y=request.y)
    await set_field(game_id, field)
    
    masked_squares = field.masked_squares()
    
    return FieldResult(squares=masked_squares)
