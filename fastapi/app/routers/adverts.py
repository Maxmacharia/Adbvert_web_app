from fastapi import APIRouter,Response, status, HTTPException, Depends
import models
import schemas
import oauth2
from typing import List, Optional
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/posts", tags=['posts'])

#Retrieve all posts
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.advert_post])
def query_advert(db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user), search: Optional[str] = ""):
    print(search)
    advert = db.query(models.Advert).filter(models.Advert.title.contains(search)).all()
    return advert


#@app.post("/users", status_code=status.HTTP_201_CREATED)
#def create_user(user : usercreate):
    #cursor.execute("""INSERT INTO usercreate(User_ID, username, email, role, password) VALUES(%s, %s, %s, %s, %s) RETURNING *""", (user.User_ID, user.username, user.email, user.role, user.password))
    #new_user = cursor.fetchone()
    #conn.commit()
    #return {"data": new_user}

#creating a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.advert_post)
def advert_create(ad: schemas.advert, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #use unpack dictionary **ad.dict() to avoid lots of texting
    print(current_user.id)
    new_post = models.Advert(owner_id = current_user.id, **ad.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#Retrieving a post by id
@router.get("/{id}", response_model=schemas.advert_post)
def get_one_post(id: int, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    one_post = db.query(models.Advert).filter(models.Advert.adid == id).first()
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    return one_post


#@app.get("/posts")
#def get_posts():
    #cursor.execute("""SELECT * FROM usercreate""")
    #posts = cursor.fetchall()
    #return posts

#Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post = db.query(models.Advert).filter(models.Advert.adid == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform the requested action")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Update a post
@router.put("/{id}", response_model=schemas.advert_post)
def update_post(id : int, updated_post: schemas.advert, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post_update = db.query(models.Advert).filter(models.Advert.adid == id)
    post = post_update.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"path with id {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform the requested action")
    post_update.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_update.first()