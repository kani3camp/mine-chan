from fastapi import FastAPI
import firebase_admin
from firebase_admin import firestore

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
