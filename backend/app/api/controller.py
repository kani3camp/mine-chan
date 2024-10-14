from .db.redis import add_hello, read_hello
from fastapi import APIRouter
from .game.controller import game_router

api_router = APIRouter(prefix='/api')
api_router.include_router(game_router)


@api_router.get('/', name='redisでアクセス履歴を追加')
async def root():
    await add_hello()
    hello = await read_hello()
    return hello

