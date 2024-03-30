from .schema import CreateGame, PlayGame, FieldResult
from .model import Game, Field, Vertex
from app.db.db import games_collection
from .model import in_field

from fastapi import APIRouter, HTTPException

from ...db import db
from ...db.db import write_field
from ...db.redis import read_game

game_router = APIRouter(prefix='/game', tags=['game'])


@game_router.get('/', name='ゲーム一覧を取得する')
async def get_games():
    pass


@game_router.post("/", name='ゲームを作成する')
async def create_game(request: CreateGame):
    new_game_ref = games_collection.document()
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
        x=request.x,
        y=request.y,
        mines=list(),
        flags=list(),
        opens=list(),
    )
    
    # 地雷を配置
    await write_field(field.to_dict())
    
    return


@game_router.post("/{game_id}", name='マスを開ける')
async def dig(game_id: str, request: PlayGame) -> FieldResult:
    field: Field | None = await db.read_field(game_id=game_id)
    if field is None:
        raise HTTPException(status_code=404)
    if len(field.mines) == 0:
        field.init_mines(x=field.x, y=field.y, num_mines=field.num_mines, first_vertex=Vertex(request.x, request.y))
        await db.update_field_mines(game_id=game_id, mines=field.mines)
    
    if not in_field(
            v=Vertex(request.x, request.y),
            x=field.x,
            y=field.y):
        raise HTTPException(status_code=400, detail='無効なマスです')
    
    return
