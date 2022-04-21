from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hash(password: str)-> str:
    return pwd_context.hash(password)

def verify(plain_password: str, hashed_password: str):
    # return pwd_context.hash(plain_password) == hashed_password
    return pwd_context.verify(plain_password, hashed_password)