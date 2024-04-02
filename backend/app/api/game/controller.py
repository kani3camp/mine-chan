from fastapi import APIRouter, HTTPException

from .schema import CreateGame, DigSquare, FieldResult, FlagSquare
from ..db import db
from ..db.model import Game, Field, Vertex
from ..db.model import in_field
from ..db.redis import read_games, push_game, set_field, read_field

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
    return FieldResult(
        squares=field.masked_squares(),
        game_state=field.game_state(),
        mines_left=field.mines_left())


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
    
    if not in_field(
            v=Vertex(request.x, request.y),
            width=field.width,
            height=field.height):
        raise HTTPException(status_code=400, detail='無効なマスです')
    
    # 初めてマスを開ける場合は地雷を配置
    if field.squares == [''] * field.width * field.height:
        print('初回：地雷を配置')
        field.init_mines(
            width=field.width,
            height=field.height,
            num_mines=field.num_mines,
            first_vertex=Vertex(request.x, request.y))
    
    if not field.is_game_ended():
        field.dig(x=request.x, y=request.y)
    
    await set_field(game_id, field)
    
    return FieldResult(
        squares=field.masked_squares(),
        game_state=field.game_state(),
        mines_left=field.mines_left())


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
    
    if not field.is_game_ended():
        field.flag(x=request.x, y=request.y)
    
    await set_field(game_id, field)
    
    return FieldResult(
        squares=field.masked_squares(),
        game_state=field.game_state(),
        mines_left=field.mines_left())
