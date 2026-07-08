from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def generate_hash_password(password: str) -> str:
    return password_hash.hash(password)

def verity_hashed_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

