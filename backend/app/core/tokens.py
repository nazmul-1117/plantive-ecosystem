import secrets
import hashlib

def generate_secret_token() -> tuple[str, str]:
    """
    Generates a secure random verification token.
    
    Returns:
        tuple[str, str]: (raw_token, token_hash)
        - raw_token: Sent to the user via email link.
        - token_hash: SHA-256 hash stored in the database.
    """

    raw_token: str = secrets.token_urlsafe(32)
    token_hash: str = hash_token(raw_token)
    return raw_token, token_hash

def hash_token(raw_token: str) -> str:
    """
    Computes deterministic SHA-256 hash of a raw token string.

    Args:
        raw_token: a raw token in string format
    
    Returns:
        text: return hexadeciamal in string format
    """

    return hashlib.sha256(
        data = raw_token.encode("utf-8")
    ).hexdigest()