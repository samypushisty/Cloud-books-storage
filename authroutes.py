from fastapi.exceptions import HTTPException
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


authrouter = APIRouter(
    prefix="/auth",
    tags=["registration"]
)


@authrouter.post("/registration")
def registration(user: User):
    try:
        with Session(autoflush=False, bind=engine) as db:
            user = user.dict()
            user["registered_at"] = naive_utcnow()
            user["password"] = hash_password(user["password"])
            # user["id"] = 1
            stmt = insert(Users).values(**user)
            print(stmt)
            db.execute(stmt)
            db.commit()
    except:
        with Session(autoflush=False, bind=engine) as db:
            query = select(Users).where(Users.email == user["email"])
            user_information = db.execute(query).scalars().first()
            if user_information:
                return HTTPException(status_code=500, detail="email be is")
            query = select(Users).where(Users.username == user["username"])
            user_information = db.execute(query).scalars().first()
            if user_information:
                return HTTPException(status_code=500, detail="username be is")
        return "piska"


@authrouter.post("/signin")
def signin(user_sign_in: UserSignIn):
    try:
        with Session(autoflush=False, bind=engine) as db:

            query = select(Users).where(Users.email == user_sign_in.email)
            user_information = db.execute(query)
            user_information = user_information.scalars().first()
            if user_information:
                if check_password(user_information.password, user_sign_in.password):
                    return create_jwt(user_information.username, user_information.id)
                else:
                    return HTTPException(status_code=500, detail="invalid passport")
            else:
                return HTTPException(status_code=500, detail="invalid email")
    except:
        return HTTPException(status_code=500, detail="something went wrong")
