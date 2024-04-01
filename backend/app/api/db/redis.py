import json
import os
from datetime import datetime

import redis.asyncio as redis
from .model import Field

r = redis.Redis(
    host=os.environ.get('REDISHOST', 'localhost'),
    port=os.environ.get('REDISPORT', 6379),
    password=os.environ.get('REDISPASS', None),
    ssl='REDISPASS' in os.environ,
    decode_responses=True,
)


async def push_game(game_id):
    await r.lpush('games', game_id)


async def read_games():
    return await r.lrange('games', 0, -1)


async def read_field(game_id: str) -> Field | None:
    field_json: str = await r.get(f'field:{game_id}')
    if field_json is None:
        return None
    return Field.from_dict(json.loads(field_json))


async def set_field(game_id: str, field: Field):
    await r.set(f'field:{game_id}', json.dumps(field.to_dict()))


async def add_hello():
    await r.lpush('hello', datetime.now().isoformat())


async def read_hello():
    return await r.lrange('hello', 0, -1)
