from fastapi import APIRouter,Response, status, HTTPException, Depends
import models
import schemas
import oauth2
from typing import List, Optional
from database import get_db
from sqlalchemy.orm import Session
from shapely.geometry import Polygon

router = APIRouter(prefix="/polygon", tags=['polygon'])

# API endpoint to create a polygon
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreatedPolygon)
def create_polygon(polygon: schemas.PolygonCreate, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    try:
        # Create a Shapely Polygon object from the provided points
        shapely_polygon = Polygon(polygon.boundary)

        # Convert the Shapely Polygon to a WKT representation
        wkt_polygon = shapely_polygon.wkt

        # Create a new PolygonModel instance
        db_polygon = models.PolygonModel(geom=wkt_polygon, owner_id = current_user.id)

        # Add the instance to the session and commit changes to the database
        db.add(db_polygon)
        db.commit()
        db.refresh(db_polygon)

        new_polygon = {
            "id": db_polygon.id,
            "boundary": wkt_polygon,
            "created_at": db_polygon.created_at,
            "owner_id": db_polygon.owner_id,
            "owner": db_polygon.owner
        }
        return new_polygon
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create polygon: {str(e)}")
    finally:
        db.close()

    #Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    poly = db.query(models.PolygonModel).filter(models.PolygonModel.id == id)
    if poly.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    if poly.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Not authorized to perform the requested action")
    poly.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)