from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from . import dotenv,Schema

Min = dotenv.Process.ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY=dotenv.Process.JWTSECRET_KEY
ALGORITHM=dotenv.Process.JWTALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        
    else:
        expire = datetime.utcnow() + timedelta(minutes=Min)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access(token:str, credentials_exception):
 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id: str = payload.get("id")
        
        print(user_id)
        
        
        if user_id is None:
            
            raise credentials_exception
        
        
        token_data = Schema.TokenData(user_id=user_id)
        
        
    except JWTError:
        
        raise credentials_exception
    
    
    
    
    
    return token_data

def get_currentuser(token : str = Depends(oauth2_scheme)):
    
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    
    )
    
    return verify_access(token,credentials_exception)
