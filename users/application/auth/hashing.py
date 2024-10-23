from passlib.context import CryptContext

context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


def get_password_hash(password):
    return context.hash(password)


def verify_password_and_update(plain_password, hashed_password):
    return context.verify_and_update(plain_password, hashed_password)