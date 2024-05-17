import bcrypt


DIGITALS = list('1234567890')
SYMBOLS = list('!@#$%^&*()-_+=:;,./?|\\')


def hash_password(password: str) -> str:
   password_bytes = password.encode('utf-8')
   hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
   return hashed_bytes.decode('utf-8')


def does_password_match(hashed: str, password: str) -> bool:
    return hashed == hash_password(password)


def is_password_valid(password: str) -> bool:
    valid = True
    valid &= len(password) >= 8 \
        and password.lower() != password \
        and True in [n in list(password) for n in DIGITALS] \
        and True in [n in list(password) for n in SYMBOLS]
 
    return valid