import uvicorn
from fastapi import FastAPI

from dotenv import load_dotenv

from api.controller import api_router

load_dotenv()

app = FastAPI()
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, port=8080)
