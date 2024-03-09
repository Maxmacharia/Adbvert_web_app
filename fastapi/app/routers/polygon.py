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
        db_polygon = models.PolygonModel(geom=wkt_polygon, boundary=polygon.boundary, owner_id = current_user.id)

        # Add the instance to the session and commit changes to the database
        db.add(db_polygon)
        db.commit()
        db.refresh(db_polygon)

        # Eagerly load the owner relationship
        db_polygon.owner  # This will load the owner relationship eagerly

        return db_polygon
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create polygon: {str(e)}")
    finally:
        db.close()

#Retrieve all posts
@router.get("/", response_model=List[schemas.CreatedPolygon])
def get_polygons(db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    polygons = db.query(models.PolygonModel).all()
    return polygons

#Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_polygon(id: int, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    polygon = db.query(models.PolygonModel).filter(models.PolygonModel.id == id).first()
    if not polygon:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Polygon with id {id} does not exist")
    first = int(polygon.owner_id)
    second = int(current_user.id)
    if first != second:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action")

    db.delete(polygon)
    db.commit()
    return {"polygon deleted"}

#An endpoint to update a polygon
@router.put("/{polygon_id}", response_model=schemas.CreatedPolygon)
def update_polygon(polygon_id: int, polygon_update: schemas.PolygonCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        # Retrieve the polygon from the database
        db_polygon = db.query(models.PolygonModel).filter(models.PolygonModel.id == polygon_id).first()

        # Check if the polygon exists
        if db_polygon is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Polygon not found")

        # Check if the current user is the owner of the polygon
        first = int(db_polygon.owner_id)
        second = int(current_user.id)
        if first != second:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to update this polygon")

        # Update the boundary of the polygon
        db_polygon.boundary = polygon_update.boundary

        # Update the Shapely Polygon object
        shapely_polygon = Polygon(polygon_update.boundary)

        # Update the WKT representation of the polygon
        db_polygon.geom = shapely_polygon.wkt

        # Commit changes to the database
        db.commit()

        # Eagerly load the owner relationship
        db.refresh(db_polygon)
        db_polygon.owner  # This will load the owner relationship eagerly

        return db_polygon
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update polygon: {str(e)}")
    finally:
        db.close()