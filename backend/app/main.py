from fastapi import FastAPI
import firebase_admin
from firebase_admin import firestore

from app.schemas import CreateGame

app = FastAPI()

firebase_app = firebase_admin.initialize_app()
db = firestore.client()


@app.get("/hello")
def get_hello():
    config_ref = db.collection("config")
    doc_ref = config_ref.document("hello")
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return {"message": "no data"}




@app.post("/game")
def create_game(game_data: CreateGame):
    # ゲームを作成
    games = db.collection("games")
    games.add()
    
    # フィールドを作成（初期化）
    # 地雷を配置
    