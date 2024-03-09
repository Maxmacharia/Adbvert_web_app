from fastapi import APIRouter,Response, status, HTTPException, Depends
import models
import schemas
import oauth2
from typing import List, Optional
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/feedback", tags=['feedback'])

@router.post("/{post_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.posted_feedback)
def create_post(post_id: int, comment: schemas.feedback_post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Verify if the specified post exists
    post = db.query(models.Advert).filter(models.Advert.adid == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # Create the feedback with the specified post_id
    new_feedback = models.Userfeedback(owner_id=current_user.id, post_id=post_id, **comment.dict())
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    return new_feedback

#An endpoint to delete a comment
@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Verify if the specified comment exists
    comment = db.query(models.Userfeedback).filter(models.Userfeedback.feedback_id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    # Check if the user is the owner of the comment
    first = int(comment.owner_id)
    second = int(current_user.id)
    if first != second:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this comment")

    # Delete the comment
    db.delete(comment)
    db.commit()
    return None

#An endpoint that updates a comment
@router.put("/{comment_id}", response_model=schemas.posted_feedback)
def update_comment(comment_id: int, comment: schemas.feedback_post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Verify if the specified comment exists
    existing_comment = db.query(models.Userfeedback).filter(models.Userfeedback.feedback_id == comment_id).first()
    if not existing_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    # Check if the user is the owner of the comment
    first = int(existing_comment.owner_id)
    second = int(current_user.id)
    if first != second:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this comment")

    # Update the comment
    existing_comment.comments = comment.comments
    db.commit()
    db.refresh(existing_comment)
    return existing_comment

#an endpoint that fetches all comments
@router.get("/{post_id}/comments", response_model=List[schemas.posted_feedback])
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    # Verify if the specified post exists
    post = db.query(models.Advert).filter(models.Advert.adid == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Fetch all comments associated with the specified post
    comments = db.query(models.Userfeedback).filter(models.Userfeedback.post_id == post_id).all()
    
    return comments