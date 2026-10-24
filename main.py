from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.api.v1.wallets import router as wallets_router
from app.api.v1.operations import router as operations_router
from app.api.v1.users import router as users_router

from app.database import Base, engine

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "static" / "index.html"

app = FastAPI(title="Finance Tracker")

# CORS нужен, если открывать index.html не через сервер (file://) или с другого порта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wallets_router, prefix='/api/v1', tags=['wallets'])
app.include_router(operations_router, prefix='/api/v1', tags=['operations'])
app.include_router(users_router, prefix='/api/v1', tags=['users'])


@app.get("/", include_in_schema=False)
def index():
    # Фронтенд: один файл static/index.html
    return FileResponse(INDEX_FILE)


Base.metadata.create_all(bind=engine)
