from fastapi.encoders import jsonable_encoder

from auth.hash_password import hash_password, check_password
from auth.jwt_functions import create_jwt
from models.models import Users
from datafunctions import naive_utcnow
from sqlalchemy import create_engine, insert, select
from sqlalchemy.orm import Session
from config import DB_HOST, DB_PORT, DB_NAME, DB_PASS, DB_USER
from fastapi import APIRouter
from models.schemes import User, UserSignIn

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False)


router = APIRouter(
    prefix="/auth",
    tags=["registration"]
)



@router.post("/registration")
def registration(user: User):
    try:
        with Session(autoflush=False, bind=engine) as db:
            user = user.dict()
            user["registered_at"] = naive_utcnow()
            user["password"] = hash_password(user["password"])
            stmt = insert(Users).values(**user)
            print(stmt)
            db.execute(stmt)
            db.commit()
    except:
        with Session(autoflush=False, bind=engine) as db:
            query = select(Users).where(Users.email == user["email"])
            user_information = db.execute(query).scalars().first()
            if user_information:
                return "email be is"
            query = select(Users).where(Users.email == user["username"])
            user_information = db.execute(query).scalars().first()
            if user_information:
                return "username be is"



@router.post("/signin")
def signin(user_sign_in: UserSignIn):
    with Session(autoflush=False, bind=engine) as db:
        query = select(Users).where(Users.email == user_sign_in.email)
        user_information = db.execute(query)
        user_information = user_information.scalars().first()
        if user_information:
            if check_password(user_information.password, user_sign_in.password):
                return create_jwt(user_information.username)
            else:
                return "invalide passport"
        else:
            return "invalide email"
