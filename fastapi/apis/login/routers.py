from datetime import datetime, timedelta
from typing import Optional

from fastapi import Request, Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from config import settings

from apis.users.models import User
from core.hashing import Hashing
from .models import Token, TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

router = APIRouter()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    if (user := await request.app.mongodb["users"].find_one({"login.username": token_data.username})) is not None:
        return user

    raise credentials_exception
    

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user['disabled']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return current_user


@router.post("/token", response_model=Token, response_description="Login to get an access token")
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):

    if (user := await request.app.mongodb["users"].find_one({"login.username": form_data.username})) is not None:
        if Hashing.verify_password(form_data.password, user['login']['password']):
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user['login']['username']}, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
