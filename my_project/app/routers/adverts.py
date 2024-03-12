from fastapi import APIRouter,Response, status, HTTPException, Depends, BackgroundTasks
from my_project.app import models
from my_project.app import schemas
from my_project.app import oauth2
from typing import List, Optional
from my_project.app.database import get_db
from sqlalchemy.orm import Session, joinedload
from shapely.geometry import Polygon, Point


router = APIRouter(prefix="/posts", tags=['posts'])

#Retrieve all posts
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.advert])
def query_advert(db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user), search: Optional[str] = ""):
    print(search)
    advert = db.query(models.Advert).filter(models.Advert.title.contains(search)).all()
    return advert

# Creating a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.advert_post)
def advert_create(ad: schemas.advert, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        # Query the database to find the polygon_id associated with the current user
        polygon_id = db.query(models.PolygonModel.id).filter(models.PolygonModel.owner_id == current_user.id).first()
        if not polygon_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Polygon not found for the current user")

        # Create the post with the fetched polygon_id and the current user associated
        new_post = models.Advert(owner_id=current_user.id, polygon_id=polygon_id[0], **ad.dict())

        db.add(new_post)
        db.commit()

        # Explicitly load the owner and polygon attributes
        db.refresh(new_post)
        new_post.owner
        new_post.polygon

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create post: {str(e)}")
    finally:
        db.close()

    return new_post

#Retrieving a post by id
@router.get("/{id}", response_model=schemas.advert_post)
def get_one_post(id: int, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    one_post = db.query(models.Advert).filter(models.Advert.adid == id).first()
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    return one_post

# Deleting a post
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def advert_delete(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        # Query the post from the database
        post = db.query(models.Advert).filter(models.Advert.adid == post_id).first()

        # Check if the post exists
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        first = int(post.owner_id)
        second = int(current_user.id)
        # Check if the current user is the owner of the post
        if first != second:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this post")

        # Delete the post
        db.delete(post)
        db.commit()
        return {"message": "ad deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete post: {str(e)}")
    finally:
        db.close()

#Update a postraise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform the requested action")
@router.put("/{id}", response_model=schemas.advert_post)
def update_post(id : int, updated_post: schemas.advert, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post_update = db.query(models.Advert).filter(models.Advert.adid == id)
    post = post_update.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"path with id {id} does not exist")
    first = int(post.owner_id)
    second = int(current_user.id)
    if first != second:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform the requested action")
    post_update.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_update.first()