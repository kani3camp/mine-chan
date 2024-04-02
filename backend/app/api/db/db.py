from typing import Optional

from google.cloud import firestore

db = firestore.AsyncClient()

games_collection = db.collection('games')
fields_collection = db.collection('fields')
users_collection = db.collection('users')
config_collection = db.collection("config")


async def write_field(data: dict) -> None:
    field_ref = fields_collection.document()
    await field_ref.set(data)


async def read_field(game_id: str) -> Optional[dict]:
    doc_ref = fields_collection.document(game_id)
    doc = await doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None


async def update_field_mines(game_id: str, mines: list) -> None:
    doc_ref = fields_collection.document(game_id)
    await doc_ref.update({'mines': mines})
