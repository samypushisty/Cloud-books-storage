from models.models import Users
from datafunctions import naive_utcnow
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session
from config import DB_HOST, DB_PORT, DB_NAME, DB_PASS, DB_USER
from fastapi import APIRouter
from models.modelsforandpoints import User


DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=True)


router = APIRouter(
    prefix="/auth",
    tags=["registration"]
)


@router.post("/registration")
def registration(user: User):
    with Session(autoflush=False, bind=engine) as db:
        user = user.dict()
        user["registered_at"] = naive_utcnow()
        stmt = insert(Users).values(**user)
        db.execute(stmt)
        db.commit()
