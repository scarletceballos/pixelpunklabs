from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import JWTError, jwt
from database import DatabaseManager
from schemas import UserCreate, UserInDB, SessionData
import os

# Security configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class UserManager:
    def __init__(self):
        self.db = DatabaseManager()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    async def create_user(self, user: UserCreate) -> UserInDB:
        # Check if user exists
        existing_user = await self.db.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        hashed_password = self.get_password_hash(user.password)
        user_data = {
            "email": user.email,
            "username": user.username,
            "hashed_password": hashed_password
        }
        
        created_user = await self.db.create_user(user_data)
        return UserInDB(**created_user)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
            
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        # Store session
        session_data = SessionData(
            user_id=data["sub"],
            token=encoded_jwt,
            expires_at=expire
        )
        self.db.store_session(session_data.dict())
        
        return encoded_jwt

    async def authenticate_user(self, email: str, password: str) -> Optional[UserInDB]:
        user = await self.db.get_user_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user["hashed_password"]):
            return None
        return UserInDB(**user) 