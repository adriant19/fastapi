from passlib.context import CryptContext


def hash(password: str):
    # hash passwords for security - user.password
    return CryptContext(schemes=["bcrypt"]).hash(password)
