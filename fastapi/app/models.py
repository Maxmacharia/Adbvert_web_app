from sqlalchemy import Column, Integer, String, ForeignKey
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from database import Base

class User(Base):
    __tablename__="usercreate"
    userid = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))


class Advert(Base):
    __tablename__ = "advertisement"
    adid = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("usercreate.userid", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")

# Define the model for the Polygon table
class PolygonModel(Base):
    __tablename__ = "polygons"

    id = Column(Integer, primary_key=True, index=True)
    geom = Column(Geometry("POLYGON"))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("usercreate.userid", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


#class Userfeedback(Base):
    #__tablename__ = "feedback"
    #feedback_id = Column(Integer, primary_key=True)
    #post_id = Column(Integer, ForeignKey("advertisement.adid", ondelete="CASCADE"), nullable=False)
    #comments = Column(String)
    #geofence = Column(Geometry("POLYGON"))
    #created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))
    #owners_id = Column(Integer, ForeignKey("usercreate.userid", ondelete="CASCADE"), nullable=False)

    #owner = relationship("Advert", "User")