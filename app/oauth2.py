import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta


SECRET_KEY = "180bcdafaf6959f3ecb1fcae87efbfcdd7c970b30b8018f823d73bdb4093021b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token
