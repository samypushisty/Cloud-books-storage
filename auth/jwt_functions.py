import time
import jwt
from config import SECRET_KEY
from datafunctions import naive_utcnow, naive_utcfromtimestamp


def create_jwt(name: str):
    return jwt.encode(payload={'name': name, "expires": time.time() + 3600}, key=SECRET_KEY, algorithm='HS256')


def verefy_jwt(jwt_key: str):
    try:
        data = jwt.decode(jwt_key, SECRET_KEY, algorithms=["HS256"])
        expire = data.get("expires")
        if expire is None:
            return False
        if naive_utcnow() > naive_utcfromtimestamp(expire):
            return False
        return True
    except:
        return False


print(verefy_jwt(create_jwt("vlad")))
