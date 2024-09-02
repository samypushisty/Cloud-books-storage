from fastapi.exceptions import HTTPException
from auth.jwt_functions import verefy_jwt, check_valid
from models.models import Books, UsersToBooks
from sqlalchemy import create_engine, insert, select
from sqlalchemy.orm import Session
from config import DB_HOST, DB_PORT, DB_NAME, DB_PASS, DB_USER
from fastapi import APIRouter
from models.schemes import AddBook



id_book_base = []

def reload_book_bd_id():
    with Session(autoflush=False, bind=engine) as db:
        try:
            query = select(Books.id)
            result = db.execute(query)
            global id_book_base
            id_book_base = [row[0] for row in result]
            print(id_book_base)
        except:
            pass



DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False)


interfacerouter = APIRouter(
    prefix="/commands",
    tags=["usercomands"]
)


@interfacerouter.post("/addbook")
def addbook(book: AddBook, jwt: str):
    book = book.dict()
    jwt_info = verefy_jwt(jwt)
    valid_info = check_valid(jwt_info, "watch_books")
    if valid_info["value"] is True:
        with Session(autoflush=False, bind=engine) as db:
            try:
                stmt = insert(Books).values(**book)
                db.execute(stmt)
                db.commit()
                reload_book_bd_id()
            except:
                return HTTPException(status_code=500, detail="book is be")
    else:
        return HTTPException(status_code=500, detail=valid_info["information"])


@interfacerouter.post("/addbooktofavoritelist")
def addbooktofavoritelist(book_id: int, jwt: str):
    jwt_info = verefy_jwt(jwt)
    valid_info = check_valid(jwt_info, "watch_books")
    if valid_info["value"] is True:
        with Session(autoflush=False, bind=engine) as db:
            try:
                stmt = insert(UsersToBooks).values({
                    "user_id": jwt_info["id"],
                    "book_id": book_id
                })
                db.execute(stmt)
                db.commit()
            except:
                return HTTPException(status_code=500, detail="book or user is not be")
    else:
        return HTTPException(status_code=500, detail=valid_info["information"])


@interfacerouter.post("/3books/{page}")
def page_with_books(page: int, jwt: str):
    jwt_info = verefy_jwt(jwt)
    valid_info = check_valid(jwt_info, "watch_books")
    if valid_info["value"] is True:
        with Session(autoflush=False, bind=engine) as db:
            try:
                if page*3-3 < len(id_book_base):
                    if page*3 < len(id_book_base):
                        first_id = page*3-3
                        last_id = page*3-1
                    else:
                        first_id = page * 3 - 3
                        last_id = len(id_book_base)-1
                    query = select(Books).filter(id_book_base[first_id] <= Books.id).filter(Books.id <= id_book_base[last_id])
                    result = db.execute(query)
                    return [{key: value for key, value in zip(['title', 'id'], [row[0].title, row[0].id])} for row in result]

            except:
                return HTTPException(status_code=500, detail="books is none")
    else:
        return HTTPException(status_code=500, detail=valid_info["information"])


@interfacerouter.post("/book")
def watch_book(book_id: int, jwt: str):
    jwt_info = verefy_jwt(jwt)
    valid_info = check_valid(jwt_info, "watch_books")
    if valid_info["value"] is True:
        with Session(autoflush=False, bind=engine) as db:
            try:
                query = select(Books).filter(Books.id == book_id)
                return db.execute(query).scalars().all()
            except:
                return HTTPException(status_code=500, detail="book is not be")
    else:
        return HTTPException(status_code=500, detail=valid_info["information"])


@interfacerouter.post("/WatchFavoriteList")
def watch_favorite_list(jwt: str):
    jwt_info = verefy_jwt(jwt)
    valid_info = check_valid(jwt_info, "watch_books")
    if valid_info["value"] is True:
        with Session(autoflush=False, bind=engine) as db:
            try:
                query = select(UsersToBooks.book_id).filter(UsersToBooks.user_id == jwt_info["id"])
                return db.execute(query).scalars().all()
            except:
                return HTTPException(status_code=500, detail="book is not be")
    else:
        return HTTPException(status_code=500, detail=valid_info["information"])
