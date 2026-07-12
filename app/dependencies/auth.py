from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.config.config import get_settings

settings = get_settings()
security = HTTPBearer()
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials   # <-- ИЗВЛЕКАЕМ СТРОКУ
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = UserRepository(db).get_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user

def get_current_user_optional(token: str = Depends(security), db: Session = Depends(get_db)):
    try:
        return get_current_user(token, db)

    except HTTPException:
        return None