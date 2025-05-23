import time
from sqlalchemy.orm import Session
from fastapi import FastAPI, Query, HTTPException, status, Depends, APIRouter
from pydantic import BaseModel
from database import engine, get_db
import models, schema, oauth
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List
from sqlalchemy import func


router = APIRouter( tags=["Posts"])

while True:
    try:
        conn = psycopg2.connect(

            host="localhost",
            database="products",
            user="postgres",
            password='123',
            port='5000',
            cursor_factory= RealDictCursor
        ) 

        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as e:
        print("Unable to connect to the database.", e)
              
        time.sleep(2)

@router.get('/posts')
def get_posts():
    posts = cursor.execute('SELECT * FROM "Posts"')
    print("posts", posts)
    return cursor.fetchall()


 
@router.get('/posts/{id}')
def get_post_by_id(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found.")
    return {"data":post}

@router.put('/update/posts/{id}')
def update_by_id(id:int, post:schema.Post, current_user:int = Depends(oauth.get_current_user)):
    cursor.execute(''' 
UPDATE "Posts" SET title=%s, content=%s, published = %s WHERE ID = %s  RETURNING *
''', (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found.")
    return {"data":post}

@router.patch('/posts/{id}')
def update_post(id:int, post:schema.updated_base_model, current_user:int = Depends(oauth.get_current_user)):
    
    row_to_update = []

    values = []

    if post.title:
        row_to_update.append('title = %s')
        values.append(post.title)
    if post.content:
        row_to_update.append('content = %s')
        values.append(post.content)
    if post.published:
        row_to_update.append('published = %s')
        values.append(post.published)

    if not row_to_update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    values.append(id) 
    query = f"UPDATE \"Posts\" SET {', '.join(row_to_update)} WHERE id = %s RETURNING *"
    cursor.execute(query, tuple(values))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found.")
    return {"data":post}       
   
@router.post("/blogs")
def create_post(post: schema.Post, db: Session = Depends(get_db) ,current_user:int = Depends(oauth.get_current_user) ):

     

        print("current_user", current_user.id)
        new_post = models.Post(owner_id = current_user.id, **post.model_dump())

        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return {"data": new_post}
    
    # except Exception as e:
    #     conn.rollback()
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"Database error: {str(e)}"
    #     )

    # try:
    #     cursor.execute(
    #         '''INSERT INTO "Posts" (title, content, published) 
    #            VALUES (%s, %s, %s) 
    #            RETURNING *''',
    #         (post.title, post.content, post.published)
    #     )
    #     new_post = cursor.fetchone()
    #     conn.commit()
    #     return {"data": new_post}
    # except Exception as e:
    #     conn.rollback()
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"Database error: {str(e)}"
    #     )
    
@router.delete('/posts/{id}')
def delete_post(id:int, db: Session = Depends(get_db), current_user:int = Depends(oauth.get_current_user)):


    post = db.query(models.Post).filter(models.Post.id == id).first()
   
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    db.delete(post)
    db.commit()
    return {"message": f"Post with id: {id} was deleted successfully."}

@router.get('/my_posts', response_model= List[schema.PostOut])
def get_my_posts(db:Session=Depends(get_db), current_user:int=Depends(oauth.get_current_user) ):
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    postvote = db.query(models.Post, func.count(models.vote.post_id).label("votes")).outerjoin(models.vote, models.Post.id == models.vote.post_id).group_by(models.Post.id).all()
    print("postvote", postvote)

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found for this user.")
    # return posts
    return postvote