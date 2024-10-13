import uvicorn
from fastapi import FastAPI

from dotenv import load_dotenv

from .api.controller import api_router
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()
# CORSを回避するために追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "https://mine-chan.web.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, port=8080)
