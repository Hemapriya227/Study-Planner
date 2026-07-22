from datetime import datetime, timedelta
from typing import Optional
import jwt
from app.config import settings
from app.schemas import TokenData


def create_access_token(user_id: int) -> str:
    """
    Create JWT access token for user.
    
    Args:
        user_id: User's database ID
        
    Returns:
        Encoded JWT token string
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        "iat": datetime.utcnow()
    }
    
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return token


def decode_access_token(token: str) -> Optional[TokenData]:
    """
    Decode and verify JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        TokenData object if valid, None if expired/invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: int = payload.get("user_id")
        
        if user_id is None:
            return None
            
        return TokenData(user_id=user_id)
        
    except Exception as e:
        print("JWT ERROR:",type(e).__name__)
        print(e)
        return None