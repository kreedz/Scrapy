from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import settings


DeclarativeBase = declarative_base()

def db_connect():
    return create_engine(URL(**settings.DATABASE))

def create_habrahabr_table(engine):
    DeclarativeBase.metadata.create_all(engine)

def delete_from_habrahabr_table(engine, Session):
    session = Session()
    try:
        session.query(HabrahabrModel).delete()
        session.commit()
    except:
        session.rollback()


class HabrahabrModel(DeclarativeBase):
    __tablename__ = 'habrahabr'
    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    #image_urls = Column('image_urls', String)
    #images = Column('images', String)
