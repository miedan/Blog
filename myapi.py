from fastapi import FastAPI, Query, HTTPException, status, Depends
from pydantic import BaseModel
from enum import Enum
from typing import Annotated
from fastapi.params import Body
import time
import psycopg2
from psycopg2.extras import RealDictCursor
import models, schema, utils
from database import engine, Base, get_db
from sqlalchemy.orm import Session
from routes import posts, users, auth, votes



fastapi  = FastAPI()

 
models.Base.metadata.create_all(bind=engine)




fastapi.include_router(posts.router)
fastapi.include_router(users.router)
fastapi.include_router(auth.router)
fastapi.include_router(votes.router)



@fastapi.get("/sqlalchemy")
def test_sqlalchemy(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"message": "successfully connected to sqlalchemy", "data": posts}




