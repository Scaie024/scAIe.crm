import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

# Secret key for JWT (in production, use a more secure method)
SECRET_KEY = os.getenv("SECRET_KEY", "scaie_secret_key_for_development")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))  # 24 hours

class AuthService:
    def authenticate_user(self, username: str, password: str) -> bool:
        """
        Authenticate user with simple username/password check.
        For development, we'll use admin/admin.
        In production, use a proper user database.
        """
        # Simple authentication for development
        # In production, check against a user database
        return username == "admin" and password == "admin"
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create access token for authenticated user.
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[dict]:
        """
        Verify JWT token.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

# Global instance
auth_service = AuthService()