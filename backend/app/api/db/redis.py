import os
from datetime import datetime

import redis.asyncio as redis

r = redis.Redis(
    host=os.environ.get('REDISHOST', 'localhost'),
    port=os.environ.get('REDISPORT', '6379'),
    decode_responses=True)


async def read_games():
    return await r.lrange('games', 0, -1)


async def read_game(game_id):
    pass


async def add_hello():
    await r.lpush('hello', datetime.now().isoformat())


async def read_hello():
    return await r.lrange('hello', 0, -1)

