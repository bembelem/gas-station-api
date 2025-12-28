from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import setup_routers
import uvicorn

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

# Добавляем все ручки в приложение
setup_routers(app)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)