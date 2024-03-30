from datetime import datetime

import redis.asyncio as redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


async def read_games():
    return await r.lrange('games', 0, -1)


async def write_game():
    pass


async def read_game(game_id):
    pass




async def add_hello():
    await r.lpush('hello', datetime.now().isoformat())


async def read_hello():
    return await r.lrange('hello', 0, -1)
