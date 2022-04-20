from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hash(password: str):
    print(type(pwd_context.hash(password)))
    return pwd_context.hash(password)
