from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schema, utils, oauth
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])

@router.post('/login', status_code=status.HTTP_200_OK)
def login( user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    # create a token for the user
    access_token = oauth.create_acess_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
    
