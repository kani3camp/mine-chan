import datetime

from fastapi import FastAPI
from google.cloud import firestore

from app.core import init_field
from app.schemas import CreateGame, Game, Field

app = FastAPI()

db = firestore.AsyncClient()

games_collection = db.collection('games')
fields_collection = db.collection('fields')
users_collection = db.collection('users')
config_collection = db.collection("config")


test_list = list()


@app.get('/')
async def root():
    test_list.append(datetime.datetime.now())
    return test_list


@app.get("/hello")
async def get_hello():
    doc_ref = config_collection.document("hello")
    doc = await doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return {"message": "no data"}


@app.post("/game")
async def create_game(request: CreateGame):
    # ゲームを作成
    new_game_ref = games_collection.document()
    game = Game(
        game_id=new_game_ref.id,
        num_players=request.num_player,
        num_mines=request.num_mines,
        created_by=firestore.SERVER_TIMESTAMP
    )
    await new_game_ref.set(dict(game))
    
    # フィールドを作成（初期化）
    field = Field(
        game_id=new_game_ref.id,
        x=request.x,
        y=request.y,
        mines=init_field(
            x=request.x,
            y=request.y,
            num_mines=request.num_mines
        ),
        flags=list(),
        opens=list(),
    )
    
    # 地雷を配置
    field_ref = fields_collection.document()
    await field_ref.set(dict(field))
    
    return
