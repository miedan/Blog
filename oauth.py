from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
import schema, database, models
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2400

def create_acess_token(data:dict):

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_acess_token(token:str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = schema.token_data(id  =id)

    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(db: Session = Depends(database.get_db), token:str = Depends(oauth2_scheme)):
    credentials_exception= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token = verify_acess_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user




