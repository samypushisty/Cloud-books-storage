from models.models import users
from datafunctions import naive_utcnow
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session
from config import DB_HOST, DB_PORT, DB_NAME, DB_PASS, DB_USER
from fastapi import APIRouter
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

router = APIRouter(
    prefix="/auth",
    tags=["registration"]
)


@router.post("/registration")
def registration(id: int, email: str, username: str, password: str, role_id: int):
    user = {"id": id, "email": email, "username": username, "password": password, "registered_at": naive_utcnow(), "role_id": role_id}
    with Session(autoflush=False, bind=engine) as db:
        stmt = insert(users).values(**user)
        db.execute(stmt)
        db.commit()
