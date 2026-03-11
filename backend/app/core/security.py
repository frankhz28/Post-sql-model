from pwdlib import PasswordHash

pwd_contex = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return pwd_contex.hash(password)
