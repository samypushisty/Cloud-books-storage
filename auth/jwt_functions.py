import time
import jwt
from config import SECRET_KEY
from datafunctions import naive_utcnow, naive_utcfromtimestamp
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from config import DB_HOST, DB_PORT, DB_NAME, DB_PASS, DB_USER

from models.models import Roles, Users

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False)


def create_jwt(name: str, id: int):
    return jwt.encode(payload={'name': name, "expires": time.time() + 3600, 'id': id},
                      key=SECRET_KEY, algorithm='HS256')


def verefy_jwt(jwt_key: str):
    try:
        data = jwt.decode(jwt_key, SECRET_KEY, algorithms=["HS256"])
        expire = data.get("expires")
        if expire is None:
            return {
                "value": False,
                "information": "data expire is none"
            }
        if naive_utcnow() > naive_utcfromtimestamp(expire):
            return {
                "value": False,
                "information": "expired"
            }
        return {
            "value": True,
            "id": data.get("id")

        }
    except:
        return {
            "value": False,
            "information": "invalid token"
        }


def verify_transaction(id: int, permission: str):
    with Session(autoflush=False, bind=engine) as db:
        query = select(Users).where(Users.id == id)
        user_information = db.execute(query)
        user_information = user_information.scalars().first()

        query = select(Roles).where(Roles.id == user_information.role_id)
        role_information = db.execute(query)
        role_information = role_information.scalars().first()
        if role_information:
            role_permission = role_information.permissions
            if role_permission[permission]:
                return {
                    "value": True,
                    "information": "allgood"
                }
            else:
                return {
                    "value": False,
                    "information": "you have not permission"
                }
        else:
            return {
                    "value": False,
                    "information": "roll is None"
                }


def check_valid(jwt_info: dict, permission: str):
    try:
        if jwt_info["value"]:

            transaction = verify_transaction(jwt_info["id"], permission)

            if transaction["value"]:
                return {
                    "value": True
                }
            else:
                return {
                    "value": False,
                    "information": transaction["information"]
                }
        else:
            return {
                    "value": False,
                    "information": jwt_info["information"]
                }
    except:
        return {
                    "value": False,
                    "information": "something went wrong"
                }