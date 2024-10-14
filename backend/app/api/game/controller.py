from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .schema import CreateGame, DigSquare, FieldResult, FlagSquare
from ..db import model
from ..db.db import get_db
from ..db.model import Field, Vertex
from ..db.model import in_field
from ..db.redis import read_games, push_game, set_field, read_field

game_router = APIRouter(prefix='/game', tags=['game'])


@game_router.get('/', name='ゲーム一覧を取得する')
async def get_games() -> list[str]:
    games = await read_games()
    return games


@game_router.get("/{game_id}", name='ゲームを取得する')
async def get_game(game_id: int) -> FieldResult:
    field = await read_field(game_id)
    if field is None:
        raise HTTPException(status_code=404)
    return FieldResult(
        squares=field.masked_squares(),
        game_state=field.game_state(),
        mines_left=field.mines_left())


@game_router.post("/", name='ゲームを作成する')
async def create_game(request: CreateGame, rdb: AsyncSession = Depends(get_db)) -> int:
    new_game = model.Game(
        num_players=request.num_player,
        num_mines=request.num_mines,
    )
    rdb.add(new_game)
    try:
        await rdb.commit()
        await rdb.refresh(new_game)
    except IntegrityError:
        await rdb.rollback()
        raise HTTPException(status_code=400, detail='TODO') # TODO

    # フィールドを作成（初期化）
    field = model.Field(
        game_id=new_game.game_id,
        num_mines=request.num_mines,
        width=request.x,
        height=request.y,
        squares=[''] * request.x * request.y,
    )
    rdb.add(field)   # TODO: db.pyの関数を使うようにする
    try:
        await rdb.commit()
        await rdb.refresh(field)
    except IntegrityError:
        await rdb.rollback()
        raise HTTPException(status_code=400, detail='TODO') # TODO
    
    # 地雷を配置
    await set_field(new_game.game_id, field)
    await push_game(new_game.game_id)
    
    return new_game.game_id


@game_router.post("/{game_id}/dig", name='マスを開ける')
async def dig(game_id: int, request: DigSquare) -> FieldResult:
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
async def flag(game_id: int, request: FlagSquare) -> FieldResult:
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
