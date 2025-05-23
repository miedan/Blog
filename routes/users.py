
from sqlalchemy.orm import Session
import models, schema, utils
from fastapi import HTTPException, status, Depends, APIRouter
from database import  get_db


router = APIRouter(tags=["Users"])

@router.post('/signup', response_model=schema.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user:schema.Users, db:Session = Depends(get_db)):
    hashed_password= utils.hash(user.password)
    user.password = hashed_password 
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user/{id}', response_model=schema.UserOut, status_code=status.HTTP_200_OK)
def get_user(id:int, db:Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id: {id} was not found.")
    return user
