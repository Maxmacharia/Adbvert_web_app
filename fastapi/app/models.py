from sqlalchemy import Column, Integer, String, ForeignKey
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base

class User(Base):
    __tablename__="usercreate"
    userid = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))


# Define the model for the Polygon table
class PolygonModel(Base):
    __tablename__ = "polygons"

    id = Column(Integer, primary_key=True, index=True)
    geom = Column(Geometry("POLYGON"))
    boundary = Column(JSONB)  # Add boundary as JSONB type
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("usercreate.userid", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", lazy="selectin")

class Advert(Base):
    __tablename__ = "advertisement"
    adid = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("usercreate.userid", ondelete="CASCADE"), nullable=False)
    polygon_id = Column(Integer, ForeignKey("polygons.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", lazy="selectin")
    polygon = relationship("PolygonModel", lazy="selectin")


class Userfeedback(Base):
    __tablename__ = "feedback"
    feedback_id = Column(Integer, primary_key=True)
    comments = Column(String)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("usercreate.userid", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("advertisement.adid", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", lazy="selectin")
    post = relationship("Advert", lazy="selectin")