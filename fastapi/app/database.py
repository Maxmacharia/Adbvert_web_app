from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from sqlalchemy.orm import Session
import time
from config import settings

#connection with te database
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

#Creating an engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#creating an instance of the sessionLocal class to be a database session. The class itself can't be a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Function that returns a class whic will later be used to create database models and classes
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#while True:
    #try:
        #conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='BCAJWZ4496', cursor_factory=RealDictCursor)
        #cursor = conn.cursor()
        #print("Database connection successful!")
        #break
    #except Exception as error:
        #print("Database connection failed!")
        #print("Error:", error)
        #time.sleep(4)