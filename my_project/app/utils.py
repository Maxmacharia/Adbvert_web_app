from passlib.context import CryptContext

#informing passlib the default hashing algorithm which is bbcrypt in this case
pwd_content = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(password: str):
    return pwd_content.hash(password)

def verify(login_password, hashed_password):
    return pwd_content.verify(login_password, hashed_password)