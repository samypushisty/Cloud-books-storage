from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    username: str
    password: str
    role_id: int
