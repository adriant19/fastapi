from passlib.context import CryptContext

""" UTILITIES

    - additional functions used to authenticate users and privatise passwords
    via hashing
"""

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_pwd(password: str):

    # hash passwords for security - user.password
    return pwd_context.hash(password)


def verify_pwd(plain_pwd, hash_pwd):

    # check between user input password and stored hashed password
    return pwd_context.verify(plain_pwd, hash_pwd)
