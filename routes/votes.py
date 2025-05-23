from sqlalchemy.orm import Session
import models, schema, utils, oauth
from fastapi import HTTPException, status, Depends, APIRouter
from database import  get_db

router = APIRouter(tags=["votes"])

@router.post('/votes', status_code=status.HTTP_201_CREATED)
def create_vote(vote:schema.vote, db:Session= Depends(get_db), current_user:int = Depends(oauth.get_current_user)):
    
    voted_post = db.query(models.vote).filter(models.Post.id == vote.post_id, models.User.id == current_user.id).first()


    
    if vote.dir == True:
        if voted_post:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user has already voted for this post")
        
        vote = models.vote(post_id= vote.post_id, user_id= current_user.id)
        db.add(vote)
        db.commit()
        db.refresh(vote)
        return {"data": vote}
    else:
        if not voted_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user has not voted for this post")
        
        db.query(models.vote).filter(models.Post.id == vote.post_id, models.User.id == current_user.id).delete(synchronization= False)
        db.commit()
        return {"message":"vote sucessfully deleted"}
    
    # get votes for a specific votes 

    # @router.get('/votes/{id}', response_model = List[Schema.vote])